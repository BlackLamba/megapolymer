from app.db.session import SessionLocal
from fastapi import Depends, HTTPException
from app.core.security import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = decode_token(token)
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")