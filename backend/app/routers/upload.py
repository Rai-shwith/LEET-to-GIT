from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException, status, Request
from app.schemas import Uploads
from app.dependencies import get_current_user, get_db
from app.security import get_token_from_cookie, decrypt_token
from app.models import User
from app.config import settings
import asyncio
import os
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
from scripts.output_content_creator import output_content_creator_for_batch_upload
from scripts.github_handler.batch_upload import batch_upload_files
from scripts.github_handler.upload_file import get_repo_readme_for_manual
from scripts.LeetcodeBrowserTasks.get_js_snippet import generate_browser_snippet
from github import Github, Auth
from scripts.logging_config import logger

router = APIRouter(tags=["Upload"])

# Dictionary to hold mappings: connection_id -> UI WebSocket
webSocketConnections = {}

automatic_websocket_messages = [
    "Code sent successfully. Copy and paste it in the Leetcode console.",
    "Leetcode data received",
    "Processing the data...",
    "Uploading the data to github...",
    "Upload successful checkout your repository"
]

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

async def get_ws_user(websocket: WebSocket, db: AsyncSession):
    # Retrieve the token from headers or cookies
    token = websocket.cookies.get("github_token")
    if not token:
        return None
    try:
        decrypted_token = decrypt_token(token)
    except Exception:
        return None

    # Verify with GitHub
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {decrypted_token}", "Accept": "application/vnd.github.v3+json"}
        )
    if response.status_code != 200:
        return None
        
    user_data = response.json()
    github_id = user_data["id"]

    # Verify with database
    stmt = select(User).where(User.github_id == github_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    return user

@router.websocket("/ws/automatic/")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    
    user = await get_ws_user(websocket, db)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Secure Connection management
    connection_id = str(user.id)
    webSocketConnections[connection_id] = websocket
    
    # Establish WebSocket Domain matching environment
    if hasattr(settings, 'domain') and settings.domain:
        websocket_domain = f'wss://{settings.domain}/upload/ws/automatic/'
    else:
        websocket_domain = 'ws://localhost:8000/upload/ws/automatic/'

    try:
        # Generate the javascript string using the secure connection_id
        js_snippet = generate_browser_snippet(websocket_domain, connection_id)
        
        await websocket.send_json({
            "code": js_snippet,
            "message": automatic_websocket_messages[0],
            "error": False
        })

        while True:
            # Keep pinging to keep UI WS alive
            await asyncio.sleep(30)
            await websocket.send_json({"ping": True})
            pong = await websocket.receive_text()
            
    except WebSocketDisconnect:
        if connection_id in webSocketConnections:
            del webSocketConnections[connection_id]
        logger.info(f"UI Client #{connection_id} disconnected")

@router.websocket("/ws/automatic/{connection_id}")
async def automatic_uploads(websocket: WebSocket, connection_id: str, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    
    if connection_id not in webSocketConnections:
        logger.error("Invalid Connection ID")
        await websocket.send_json({"message": "Invalid Connection ID", "error": True})
        return await websocket.close()
        
    logger.info("Browser extension script connected to secondary socket.")
    ui_websocket: WebSocket = webSocketConnections[connection_id]
    
    try:
        # Wait for LeetCode submissions JSON output from JS 
        data = await websocket.receive_text()
        logger.info(f"Data received from Automatic Console Script")
        
        await ui_websocket.send_json({
            "message": automatic_websocket_messages[1],
            "error": False
        })
        
        data = json.loads(data)
        uploads: Uploads = Uploads(uploads=data["uploads"])
        
        await ui_websocket.send_json({
            "message": automatic_websocket_messages[2],
            "error": False
        })
        
        # User auth loading
        user = await get_ws_user(ui_websocket, db)
        if not user:
            raise Exception("User cookie expired during processing")
            
        token = ui_websocket.cookies.get("github_token")
        decrypted_token = decrypt_token(token)
        auth = Auth.Token(decrypted_token)
        g = Github(auth=auth)

        # Start Processing files
        file_structure = output_content_creator_for_batch_upload(uploads=uploads)
        github_user = await asyncio.to_thread(g.get_user)
        repo = await asyncio.to_thread(github_user.get_repo, user.repo_name)
        
        await ui_websocket.send_json({
            "message": automatic_websocket_messages[3],
            "error": False
        })
        
        repo_readme_content = await asyncio.to_thread(
            get_repo_readme_for_manual,
            repo,
            github_user.login,
            user.repo_name,
            uploads
        )
        file_structure["README.md"] = repo_readme_content
        
        await asyncio.to_thread(batch_upload_files, repo, file_structure, "Automated bulk upload of Leetcode solutions")
        
        await ui_websocket.send_json({
            "message": f"Upload successful. Added solutions to github.com/{github_user.login}/{user.repo_name}",
            "error": False
        })
        
        # Explicit disconnect handling
        await db.commit()
        await websocket.close()
        
    except WebSocketDisconnect:
        logger.info("Browser script websocket disconnected")
    except Exception as e:
        logger.error(f"Error processing automatic upload: {e}")
        try:
            await ui_websocket.send_json({
                "message": f"Processing failed: {str(e)}",
                "error": True
            })
        except:
            pass
