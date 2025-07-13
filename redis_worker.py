import asyncio, logging, threading
from app.queue.redis_queue import pop_task
from app.tasks.groq_task import handle_groq_task
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("redis-worker")

# ✅ Dummy HTTP server to satisfy Render's port scan
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Redis worker is running")

def run_http_server():
    server = HTTPServer(("0.0.0.0", 10000), DummyHandler)
    log.info("Dummy HTTP server started on port 10000")
    server.serve_forever()

# ✅ Redis worker async loop
async def redis_worker_loop():
    log.info("Redis worker started …")
    while True:
        task = pop_task(timeout=5)
        if task:
            log.info("Got task %s", task["id"])
            handle_groq_task(
                chatroom_id=task["chatroom_id"],
                message_id=task["message_id"],
                prompt=task["prompt"]
            )
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    # Start dummy HTTP server in a background thread
    threading.Thread(target=run_http_server, daemon=True).start()

    # Start Redis task processor
    asyncio.run(redis_worker_loop())
