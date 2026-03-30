from sqlalchemy import Column, Integer, String, BigInteger, Text, TIMESTAMP, text
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    avatar_url = Column(Text, nullable=True)
    github_id = Column(BigInteger, nullable=False, unique=True)
    repo_name = Column(String(255), nullable=False, default="LeetCode")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()"))