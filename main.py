from fastapi import FastAPI
from app.api import auth
from app.db.database import Base, engine
from app.api import auth, chatroom ,message ,subscription
from app.api.webhook import router as webhook_router
from app.api.stripe_page import router as stripe_page_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(chatroom.router)
app.include_router(message.router)
app.include_router(subscription.router)
app.include_router(webhook_router)
app.include_router(stripe_page_router)