from cryptography.fernet import Fernet
from fastapi import Request, HTTPException, status
from app.config import settings
import logging

key = settings.ENCRYPTION_KEY
salt = settings.ENCRYPTION_SALT

def encrypt_token(token: str) -> str:
    f = Fernet(key.encode())
    return f.encrypt((token + salt).encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    try:
        f = Fernet(key.encode())
        decrypted = f.decrypt(encrypted_token.encode()).decode()
        if not decrypted.endswith(salt):
            raise ValueError("Invalid salt")
        return decrypted[:-len(salt)]
    except Exception as e:
        logging.error(f"Error decrypting token: {e}")
        raise ValueError("Invalid or corrupted token")

def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("github_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        return decrypt_token(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")