from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.routes import router
from app.core.config import settings


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="개발자를 위한 맞춤형 Q&A 시스템",
    description="RAG 기반 기술 문서 Q&A 시스템 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(router, prefix="/api/v1")

# 정적 파일 서빙 (프론트엔드용)
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    print("🚀 개발자를 위한 맞춤형 Q&A 시스템이 시작되었습니다.")
    print(f"📚 문서 디렉토리: {settings.documents_dir}")
    print(f"🗄️ 벡터 데이터베이스: {settings.chroma_persist_directory}")
    print(f"🌐 API 문서: http://localhost:{settings.port}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    print("👋 Q&A 시스템이 종료되었습니다.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    ) 