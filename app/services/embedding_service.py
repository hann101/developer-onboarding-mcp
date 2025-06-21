from typing import List
from sentence_transformers import SentenceTransformer
from app.core.config import settings


class EmbeddingService:
    """임베딩 생성 서비스"""
    
    def __init__(self):
        self.local_model = None
        self._initialize_models()
    
    def _initialize_models(self):
        """임베딩 모델 초기화"""
        try:
            # 로컬 임베딩 모델 초기화 (기본값)
            self.local_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ 로컬 임베딩 모델 초기화 완료 (sentence-transformers)")
            
        except Exception as e:
            print(f"❌ 임베딩 모델 초기화 실패: {e}")
            raise
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """텍스트 리스트에 대한 임베딩 생성"""
        try:
            return self._get_local_embeddings(texts)
                
        except Exception as e:
            print(f"❌ 임베딩 생성 실패: {e}")
            raise
    
    def _get_local_embeddings(self, texts: List[str]) -> List[List[float]]:
        """로컬 임베딩 모델로 임베딩 생성"""
        try:
            embeddings = self.local_model.encode(texts)
            return embeddings.tolist()
            
        except Exception as e:
            print(f"❌ 로컬 임베딩 생성 실패: {e}")
            raise
    
    def get_single_embedding(self, text: str) -> List[float]:
        """단일 텍스트에 대한 임베딩 생성"""
        embeddings = self.get_embeddings([text])
        return embeddings[0] if embeddings else []


# 전역 임베딩 서비스 인스턴스
embedding_service = EmbeddingService() 