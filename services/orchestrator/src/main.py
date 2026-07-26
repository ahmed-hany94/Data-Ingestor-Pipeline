import os
import sys
import time
import redis

def main():
    # connect to redis
    redis_url = os.getenv("REDIS_URL", "localhost:6379")
    host, port = redis_url.split(":")
    pool = redis.ConnectionPool(
        host=host,
        port=port,
        db=0,
        decode_responses=True,
        socket_timeout=None
    )
    r = redis.Redis(connection_pool=pool)
	# if no connection, error and quit
    try:
        if r.ping():
            print("Connected successfully!")
    except redis.exceptions.ConnectionError:
        print("Could not connect to Redis. Check if the server is running.")
        sys.exit(1)

    REDIS_QUEUE_KEY = os.getenv("REDIS_QUEUE_KEY", "data_queue")
    # poll the redis queue and BPOP if there is an event.
    while True:
        try:
            result = r.brpop(REDIS_QUEUE_KEY, timeout=0)
            task_data = result[1]
        except redis.exceptions.ConnectionError:
            print("Connection lost. Retrying in 5 seconds...")
            time.sleep(5)
    # For now forward it to the analytics server

main()