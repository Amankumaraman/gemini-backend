import os, logging, openai
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Message
from dotenv import load_dotenv
load_dotenv()

openai.api_key  = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"
MODEL_NAME      = "llama3-70b-8192"
logger          = logging.getLogger(__name__)

def handle_groq_task(chatroom_id: int, message_id: int, prompt: str):
    """Called by the Redis worker."""
    try:
        resp = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.7
        )
        ai_text = resp.choices[0].message["content"].strip()

        db: Session = SessionLocal()
        ai_msg = Message(chatroom_id=chatroom_id, sender="ai", content=ai_text)
        db.add(ai_msg)
        db.commit()
        db.close()
        logger.info("Saved Groq response for chatroom %s", chatroom_id)
    except Exception as e:
        logger.exception("Groq task failed: %s", e)
