import redis
import os
from dotenv import load_dotenv

load_dotenv()
r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

def get_cached_chatrooms(user_id: int):
    key = f"user:{user_id}:chatrooms"
    return r.get(key)

def set_cached_chatrooms(user_id: int, data: str, ttl: int = 600):
    key = f"user:{user_id}:chatrooms"
    r.set(key, data, ex=ttl)

def invalidate_cached_chatrooms(user_id: int):
    key = f"user:{user_id}:chatrooms"
    r.delete(key)
