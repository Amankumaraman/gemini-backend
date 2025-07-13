import asyncio, logging
from app.queue.redis_queue import pop_task
from app.tasks.groq_task import handle_groq_task   # path matches your project

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("redis-worker")

async def main():
    log.info("Redis worker started …")
    while True:
        task = pop_task(timeout=5)          # blocks up to 5 s
        if task:
            log.info("Got task %s", task["id"])
            handle_groq_task(
                chatroom_id = task["chatroom_id"],
                message_id  = task["message_id"],
                prompt      = task["prompt"]
            )
        await asyncio.sleep(0.1)            # yield control

if __name__ == "__main__":
    asyncio.run(main())
