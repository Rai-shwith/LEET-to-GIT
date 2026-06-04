from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, oauth, upload, post, register
from app.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Leet2Git", version="2.0.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"], allow_credentials=True, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["*"])

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(oauth.router, prefix="/auth", tags=["Auth"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(post.router)
app.include_router(register.router)
