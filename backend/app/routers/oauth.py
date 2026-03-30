from fastapi import APIRouter, Depends, Query, Request, Response, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
from app.config import settings
from app.database import get_db
from app.models import User
from app.security import encrypt_token
from app.dependencies import get_current_user
from app.schemas import UserResponse

router = APIRouter()

@router.get("/login")
async def login():
    github_url = f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}&scope=repo user:email"
    return RedirectResponse(github_url)

@router.get("/callback")
async def callback(code: str = Query(...), response: Response = Response(), db: AsyncSession = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_res = await client.post("https://github.com/login/oauth/access_token", headers={"Accept": "application/json"}, data={"client_id": settings.GITHUB_CLIENT_ID, "client_secret": settings.GITHUB_CLIENT_SECRET, "code": code})
        token_data = token_res.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="Invalid auth code")

        user_res = await client.get("https://api.github.com/user", headers={"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github.v3+json"})
        user_json = user_res.json()
        if "id" not in user_json:
            raise HTTPException(status_code=400, detail="Failed to fetch GitHub user")

        github_id = user_json["id"]
        user_name = user_json.get("login", "Unknown")
        email = user_json.get("email")
        avatar_url = user_json.get("avatar_url")

        stmt = select(User).where(User.github_id == github_id)
        user_obj = (await db.execute(stmt)).scalar_one_or_none()
        if not user_obj:
            user_obj = User(github_id=github_id, user_name=user_name, email=email, avatar_url=avatar_url)
            db.add(user_obj)
        else:
            user_obj.user_name = user_name
            user_obj.email = email
            user_obj.avatar_url = avatar_url
        await db.commit()

        encrypted = encrypt_token(access_token)
        redirect = RedirectResponse(f"{settings.FRONTEND_URL}/dashboard")
        redirect.set_cookie(key="github_token", value=encrypted, httponly=True, secure=settings.is_production, samesite="lax", max_age=3600*24)
        return redirect

@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    return user

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("github_token")
    return {"status": "logged out"}