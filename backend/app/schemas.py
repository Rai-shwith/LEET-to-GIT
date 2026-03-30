from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Union, Any

class UserResponse(BaseModel):
    id: int
    user_name: str
    email: Optional[EmailStr] = None
    github_id: int
    avatar_url: Optional[str] = None
    repo_name: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProblemDetails(BaseModel):
    questionTitle: str
    question: str
    link: str
    difficulty: str
    questionId: str
    titleSlug: str
    topicTags: List[Optional[Dict[str, Any]]]

class Solution(BaseModel):
    code_extension: str
    code: str

class Upload(BaseModel):
    question: Optional[ProblemDetails] = None
    solution: Solution

class Uploads(BaseModel):
    uploads: List[Upload]