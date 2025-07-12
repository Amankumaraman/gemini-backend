import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()  # Loads .env variables

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

celery_app.autodiscover_tasks(["app.tasks.gemini_task", "app.tasks.groq_task"])

