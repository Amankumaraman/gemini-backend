import json, os, redis, uuid, datetime as dt
from dotenv import load_dotenv
load_dotenv()

redis_url = os.getenv("REDIS_URL")          # rediss://…  or  redis://…
queue_name = "gemini_queue"

r = redis.Redis.from_url(redis_url, decode_responses=True)

def push_task(chatroom_id: int, message_id: int, prompt: str):
    """Enqueue a task as a JSON string."""
    payload = {
        "id": str(uuid.uuid4()),
        "chatroom_id": chatroom_id,
        "message_id": message_id,
        "prompt": prompt,
        "ts": dt.datetime.utcnow().isoformat()
    }
    r.rpush(queue_name, json.dumps(payload))

def pop_task(block: bool = True, timeout: int = 5):
    """Pop one task (blocking or non‑blocking)."""
    if block:
        task = r.blpop(queue_name, timeout=timeout)
        if task:                     # (key, value)
            _, val = task
            return json.loads(val)
        return None
    else:
        val = r.lpop(queue_name)
        return json.loads(val) if val else None
