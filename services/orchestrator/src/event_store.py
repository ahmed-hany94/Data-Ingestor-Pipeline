import os
import json
import logging

import psycopg2
 
logger = logging.getLogger(__name__)

class EventStore:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self._conn = None

    def connect(self):
        self._conn = psycopg2.connect(self.database_url)
        self._conn.autocommit = True

    def save(self, domain: str, payload: dict, result_ok: bool, result_data: dict) -> None:
        if self._conn is None or self._conn.closed:
            self.connect()

        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO events (domain, payload, result_ok, result_data)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (domain, json.dumps(payload), result_ok, json.dumps(result_data)),
                )
        except psycopg2.Error as exc:
            logger.error("failed to persist event to store: %s", exc)

def build_event_store() -> EventStore:
    return EventStore(database_url=os.getenv("DATABASE_URL", "localhost:5432"))