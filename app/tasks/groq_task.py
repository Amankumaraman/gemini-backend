import os
import logging
from celery import shared_task
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Message
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configure Groq OpenAI-compatible endpoint
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"
MODEL_NAME = "llama3-70b-8192"


logger = logging.getLogger(__name__)

@shared_task
def send_to_groq(chatroom_id: int, message_id: int, prompt: str):
    try:
        logger.info("Sending prompt to Groq for chatroom_id=%s", chatroom_id)

        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        ai_text = response.choices[0].message["content"].strip()

        # Save the AI message to DB
        db: Session = SessionLocal()
        ai_msg = Message(
            chatroom_id=chatroom_id,
            sender="ai",
            content=ai_text
        )
        db.add(ai_msg)
        db.commit()
        db.close()

        logger.info("Groq response saved for chatroom_id=%s", chatroom_id)

    except Exception as e:
        logger.exception("Groq task failed for chatroom_id=%s: %s", chatroom_id, str(e))
