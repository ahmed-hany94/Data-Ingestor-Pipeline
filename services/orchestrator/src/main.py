import os
import sys
import json
import time
import logging

import redis

from .event_store import build_from_env as build_event_store
from .factory import AdapterFactory, UnknownDomainError
from .strategy import EventRouter, NoRouteFound

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("orchestrator")

REDIS_QUEUE_KEY = os.getenv("REDIS_QUEUE_KEY", "data_queue")
PUBLISH_CHANNEL = os.getenv("PUBLISH_CHANNEL", "processed_events")

def connect_redis() -> redis.Redis:
    redis_url = os.getenv("REDIS_URL", "localhost:6379")
    host, port = redis_url.split(":")
    client = redis.Redis(host=host, port=int(port), db=0, decode_responses=True)

    try:
        client.ping()
    except redis.exceptions.ConnectionError:
        logger.error("could not connect to redis at %s", redis_url)
        sys.exit(1)

    logger.info("connected to redis at %s", redis_url)

    return client

def handle_event(raw_event: str, router: EventRouter, factory: AdapterFactory,
                  redis_client: redis.Redis, event_store) -> None:
    try:
        event = json.loads(raw_event)
    except json.JSONDecodeError:
        logger.error("dropping malformed event, not valid JSON: %r", raw_event)
        return

    try:
        domain = router.route(event)
    except NoRouteFound as exc:
        logger.warning("%s", exc)
        return

    try:
        adapter = factory.get(domain)
    except UnknownDomainError as exc:
        logger.error("routing/factory mismatch: %s", exc)
        return

    result = adapter.process(event)

    outgoing = {
        "domain": result.domain,
        "ok": result.ok,
        "data": result.data,
        "error": result.error,
        "source_event": event,
    }

    redis_client.publish(PUBLISH_CHANNEL, json.dumps(outgoing))
    event_store.save(
        domain=result.domain,
        payload=event,
        result_ok=result.ok,
        result_data=result.data,
    )

    if result.ok:
        logger.info("processed %s event and published result", domain)
    else:
        logger.warning("processed %s event but domain service call failed: %s",
                        domain, result.error)

def main() -> None:
    redis_client = connect_redis()
    event_store = build_event_store()
    router = EventRouter()
    factory = AdapterFactory()

    logger.info("listening on redis queue %r, publishing to channel %r",
                REDIS_QUEUE_KEY, PUBLISH_CHANNEL)

    while True:
        try:
            result = redis_client.brpop(REDIS_QUEUE_KEY, timeout=0)
            if result is None:
                continue
            _, raw_event = result
            handle_event(raw_event, router, factory, redis_client, event_store)
        except redis.exceptions.ConnectionError:
            logger.error("lost connection to redis, retrying in 5s...")
            time.sleep(5)
        except KeyboardInterrupt:
            logger.info("shutting down")
            break

main()