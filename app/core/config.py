import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# .env 파일을 명시적으로 로드
load_dotenv()


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # OpenAI 설정 (선택사항)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # Google Gemini 설정 (기본값)
    google_api_key: str
    
    # 벡터 데이터베이스 설정
    chroma_persist_directory: str = "./chroma_db"
    
    # 서버 설정
    host: str = "0.0.0.0"
    port: int = 8000
    
    # 문서 설정
    documents_dir: str = "./documents"
    max_chunk_size: int = 800
    chunk_overlap: int = 150
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 전역 설정 인스턴스
settings = Settings() 