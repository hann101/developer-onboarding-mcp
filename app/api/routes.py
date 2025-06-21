from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import os

from app.models.schemas import (
    QuestionRequest, 
    AnswerResponse, 
    DocumentUploadResponse,
    HealthResponse,
    DocumentChunk
)
from app.services.document_loader import document_loader
from app.services.embedding_service import embedding_service
from app.services.search_service import search_service
from app.services.llm_service import llm_service
from app.core.database import vector_db
from app.core.config import settings


router = APIRouter()


@router.get("/", response_model=dict)
async def root():
    """루트 엔드포인트"""
    return {
        "message": "개발자를 위한 맞춤형 Q&A 시스템 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """시스템 상태 확인"""
    try:
        db_info = vector_db.get_collection_info()
        model_info = llm_service.get_model_info()
        chunks_info = vector_db.get_chunks_info()
        
        return HealthResponse(
            status="healthy",
            database_info=db_info,
            model_info=model_info,
            chunks_info=chunks_info
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"시스템 상태 확인 실패: {str(e)}")


@router.post("/upload-documents", response_model=DocumentUploadResponse)
async def upload_documents():
    """문서 업로드 및 벡터화"""
    try:
        # 문서 디렉토리 확인
        if not os.path.exists(settings.documents_dir):
            os.makedirs(settings.documents_dir)
            return DocumentUploadResponse(
                message="문서 디렉토리가 생성되었습니다. 문서를 추가해주세요.",
                processed_files=[],
                total_chunks=0
            )
        
        # 문서 로드 및 청킹
        documents = document_loader.load_documents_from_directory()
        
        if not documents:
            return DocumentUploadResponse(
                message="처리할 문서가 없습니다.",
                processed_files=[],
                total_chunks=0
            )
        
        # 문서 내용 추출
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        # 임베딩 생성
        embeddings = embedding_service.get_embeddings(texts)
        
        # 벡터 데이터베이스에 저장
        vector_db.add_documents(texts, embeddings, metadatas)
        
        # 처리된 파일 목록
        processed_files = list(set([meta.get('source_file', 'unknown') for meta in metadatas]))
        
        return DocumentUploadResponse(
            message=f"{len(documents)}개 문서 청크가 성공적으로 처리되었습니다.",
            processed_files=processed_files,
            total_chunks=len(documents)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"문서 업로드 실패: {str(e)}")


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """질문에 대한 답변 생성"""
    try:
        # 관련 문서 검색
        search_results = search_service.search_documents(
            request.question, 
            request.max_results
        )
        
        if not search_results:
            return AnswerResponse(
                answer="죄송합니다. 질문과 관련된 문서를 찾을 수 없습니다. 다른 질문을 시도해보세요.",
                sources=[],
                confidence=0.0
            )
        
        # 가장 관련성 높은 문서 청크들 추출
        context_chunks = [result['content'] for result in search_results]
        
        # LLM을 사용한 답변 생성
        llm_response = llm_service.generate_answer(
            request.question, 
            context_chunks
        )
        
        # 소스 문서 정보 구성
        sources = []
        for result in search_results:
            sources.append(DocumentChunk(
                content=result['content'][:200] + "...",  # 미리보기
                metadata=result['metadata'],
                distance=result['distance']
            ))
        
        return AnswerResponse(
            answer=llm_response['answer'],
            sources=sources,
            confidence=llm_response['confidence']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"답변 생성 실패: {str(e)}")


@router.get("/documents/info")
async def get_documents_info():
    """문서 정보 조회"""
    try:
        return document_loader.get_document_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"문서 정보 조회 실패: {str(e)}")


@router.get("/search/statistics")
async def get_search_statistics():
    """검색 통계 정보"""
    try:
        return search_service.get_search_statistics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 통계 조회 실패: {str(e)}")


@router.post("/search/keywords")
async def search_by_keywords(keywords: List[str], max_results: int = 5):
    """키워드 기반 검색"""
    try:
        results = search_service.search_by_keywords(keywords, max_results)
        return {
            "keywords": keywords,
            "results": results,
            "total_found": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"키워드 검색 실패: {str(e)}")


@router.get("/search/optimize")
async def optimize_search_settings():
    """검색 설정 최적화 정보"""
    try:
        return {
            "optimization_features": [
                "하이브리드 검색 (벡터 + 키워드)",
                "재순위화 알고리즘",
                "동적 임계값 필터링",
                "최적화된 청킹 설정",
                "키워드 매칭 점수"
            ],
            "current_settings": {
                "chunk_size": settings.max_chunk_size,
                "chunk_overlap": settings.chunk_overlap,
                "embedding_model": "all-MiniLM-L6-v2",
                "search_algorithm": "Hybrid Search"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"최적화 정보 조회 실패: {str(e)}")


@router.get("/chunks/info")
async def get_chunks_info():
    """저장된 청크들의 상세 정보 조회"""
    try:
        chunks_info = vector_db.get_chunks_info()
        return chunks_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"청크 정보 조회 실패: {str(e)}")


@router.delete("/documents/clear")
async def clear_documents():
    """벡터 데이터베이스 초기화"""
    try:
        result = vector_db.clear_database()
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터베이스 초기화 실패: {str(e)}") 