from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/success", response_class=HTMLResponse)
async def success_page():
    return "<h1>✅ Subscription Successful</h1>"

@router.get("/cancel", response_class=HTMLResponse)
async def cancel_page():
    return "<h1>❌ Payment Canceled</h1>"
