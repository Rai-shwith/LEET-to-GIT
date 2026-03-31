from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException, status, Request
from app.schemas import Uploads
from app.dependencies import get_current_user, get_db
from app.security import get_token_from_cookie
from app.models import User
import asyncio
import os
from scripts.output_content_creator import output_content_creator_for_batch_upload
from scripts.github_handler.batch_upload import batch_upload_files
from scripts.github_handler.upload_file import get_repo_readme_for_manual
from github import Github, Auth
from scripts.logging_config import logger

router = APIRouter(tags=["Upload"])
webSocketConnections = {}

@router.post("/manual/")
async def manual_upload(
    request: Request,
    uploads: Uploads, 
    user: User = Depends(get_current_user)
):
    try:
        token = get_token_from_cookie(request)
        auth = Auth.Token(token)
        g = Github(auth=auth)

        file_structure = output_content_creator_for_batch_upload(uploads=uploads)
        
        github_user = await asyncio.to_thread(g.get_user)
        repo = await asyncio.to_thread(github_user.get_repo, user.repo_name)
        
        repo_readme_content = await asyncio.to_thread(
            get_repo_readme_for_manual,
            repo,
            github_user.login,
            user.repo_name,
            uploads
        )
        file_structure["README.md"] = repo_readme_content
        
        await asyncio.to_thread(batch_upload_files, repo, file_structure, "Automated upload: User's LeetCode solutions added in bulk")
        
        return {"pushed": len(uploads.uploads), "repo": user.repo_name}
    except Exception as e:
        logger.error(f"Error in manual_upload: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload files to GitHub")

@router.get("/ws/automatic/")
async def setup_ws_automatic(user: User = Depends(get_current_user)):
    return {"connection_id": "test_conn", "js_snippet": 'console.log("Use this to connect WS");'}
