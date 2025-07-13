# rq_worker.py
import os
from redis import Redis
from rq import Worker, Queue, Connection
from dotenv import load_dotenv

load_dotenv()  # Loads .env variables

# Connect to Redis using your environment variable
redis_url = os.getenv("REDIS_BROKER_URL")
redis_conn = Redis.from_url(redis_url)

# Define which queues to listen to
listen_queues = ['default']

# Start the worker
if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen_queues))
        worker.work()
