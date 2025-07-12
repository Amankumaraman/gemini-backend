from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.auth import *
from app.services.auth_service import send_otp, verify_otp

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(payload: UserSignup, db: Session = Depends(get_db)):
    send_otp(db, payload.mobile)
    return {"msg": "User registered, use send-otp to get OTP"}

@router.post("/send-otp", response_model=SendOtpResponse)
def send_otp_api(payload: UserSignup, db: Session = Depends(get_db)):
    otp = send_otp(db, payload.mobile)
    return {"otp": otp}

@router.post("/verify-otp", response_model=Token)
def verify_otp_api(payload: VerifyOtpRequest, db: Session = Depends(get_db)):
    token = verify_otp(db, payload.mobile, payload.otp)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return {"access_token": token, "token_type": "bearer"}
