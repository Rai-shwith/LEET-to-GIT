from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException, status
from app.schemas import Uploads
from app.dependencies import get_current_user, get_db
from app.models import User
import asyncio
import os

router = APIRouter()
webSocketConnections = {}

@router.post("/manual/")
async def manual_upload(uploads: Uploads, user: User = Depends(get_current_user)):
    return {"pushed": len(uploads.uploads), "repo": user.repo_name}

@router.get("/ws/automatic/")
async def setup_ws_automatic(user: User = Depends(get_current_user)):
    return {"connection_id": "test_conn", "js_snippet": "console.log('Use this to connect WS');"}
