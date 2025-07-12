from pydantic import BaseModel

class UserSignup(BaseModel):
    mobile: str

class SendOtpResponse(BaseModel):
    otp: str

class VerifyOtpRequest(BaseModel):
    mobile: str
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str
