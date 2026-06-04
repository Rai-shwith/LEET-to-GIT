from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
import asyncio

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.security import get_token_from_cookie
from scripts.logging_config import logger
from scripts.github_handler.create_repo import create_repo
from scripts.github_handler.get_repo import get_repo
from scripts.github_handler.get_user_info import get_user_info

router = APIRouter(tags=["Register"])

@router.get("/register/api")
async def register_user(
    request: Request,
    repo_name: str = "LeetCode",
    private: bool = True,
    new: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    This function will configure the user's Github repository in the database
    and optionally create it using PyGithub via our async threads.
    """
    logger.info("Registering user repo settings")
    logger.info(f"Repo name: {repo_name} | Private: {private} | New: {new}")
    
    # We securely fetch the PyGithub user object
    token = get_token_from_cookie(request)
    pygithub_user = await get_user_info(request=None, token=token)
    
    if new:
        # Create a new repository
        repo = await create_repo(user=pygithub_user, repo_name=repo_name, private=private)
        if repo is None:
            logger.info(f"Repo {repo_name} already exists on GitHub")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail="Repository already exists on GitHub"
            )
    else:
        # Access an existing repository
        repo = await get_repo(user=pygithub_user, repo_name=repo_name)
        if repo is None:
            logger.info(f"Repo {repo_name} not found on GitHub")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Repository not found on GitHub"
            )
            
    # Update the user's repo_name in the database
    current_user_name = current_user.user_name
    current_user.repo_name = repo_name
    db.add(current_user)
    await db.commit()
    
    logger.info(f"User {current_user_name} successfully linked repo: {repo_name}")
    return {"success": True, "repo_name": repo_name}