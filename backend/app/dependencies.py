from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.security import get_token_from_cookie
from app.models import User
import httpx

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        token = get_token_from_cookie(request)
    except HTTPException as e:
        raise e

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com/user", headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"})
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="GitHub token invalid")

    user_data = response.json()
    github_id = user_data["id"]

    stmt = select(User).where(User.github_id == github_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found in DB")

    return user