from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class QuestionRequest(BaseModel):
    """질문 요청 모델"""
    question: str
    max_results: int = 5


class DocumentChunk(BaseModel):
    """문서 청크 모델"""
    content: str
    metadata: Dict[str, Any]
    distance: float


class AnswerResponse(BaseModel):
    """답변 응답 모델"""
    answer: str
    sources: List[DocumentChunk]
    confidence: float


class DocumentUploadResponse(BaseModel):
    """문서 업로드 응답 모델"""
    message: str
    processed_files: List[str]
    total_chunks: int


class HealthResponse(BaseModel):
    """헬스 체크 응답 모델"""
    status: str
    database_info: Dict[str, Any]
    model_info: Dict[str, Any]
    chunks_info: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """에러 응답 모델"""
    error: str
    detail: Optional[str] = None 