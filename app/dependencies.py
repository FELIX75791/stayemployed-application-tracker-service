from fastapi import Depends, HTTPException
from jose import JWTError
from .services.auth_service import decode_access_token, oauth2_scheme

def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = decode_access_token(token)
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"JWTError: {e}")
    return user_email
