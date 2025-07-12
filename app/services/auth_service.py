import random
from sqlalchemy.orm import Session
from app.db.models import User
from app.core.jwt import create_access_token

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def send_otp(db: Session, mobile: str) -> str:
    otp = generate_otp()
    user = db.query(User).filter(User.mobile == mobile).first()
    if user:
        user.otp = otp
    else:
        user = User(mobile=mobile, otp=otp)
        db.add(user)
    db.commit()
    return otp

def verify_otp(db: Session, mobile: str, otp: str):
    user = db.query(User).filter(User.mobile == mobile).first()
    if user and user.otp == otp:
        user.is_verified = True
        db.commit()
        access_token = create_access_token(data={"sub": user.mobile})
        return access_token
    return None
