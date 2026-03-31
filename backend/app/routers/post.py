from typing import Optional
from fastapi import APIRouter, Query, status, HTTPException
from urllib.parse import unquote
from app import schemas
from scripts import problem_fetcher

router = APIRouter(prefix="/post", tags=["Post"])

@router.get("/api", status_code=status.HTTP_200_OK, response_model=schemas.ProblemDetails)
async def create_upload(question: Optional[str] = Query(..., description="LeetCode question URL or title")):
    if not question:
        raise HTTPException(status_code=400, detail="Missing question param")
    
    question_decoded = unquote(question)
    # Check if user entered something like "valid parenthesis" (space separated) instead of slug
    if "leetcode.com" not in question_decoded and " " in question_decoded:
        question_decoded = question_decoded.strip().replace(" ", "-").lower()
        
    problem_detail = await problem_fetcher.get_problem_details(question_decoded)
    return problem_detail
