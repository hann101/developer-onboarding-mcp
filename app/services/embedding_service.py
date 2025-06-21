from typing import List
from sentence_transformers import SentenceTransformer
from app.core.config import settings
import numpy as np


class EmbeddingService:
    """임베딩 생성 서비스"""
    
    def __init__(self):
        self.local_model = None
        self._initialize_models()
    
    def _initialize_models(self):
        """임베딩 모델 초기화"""
        try:
            # 기존 벡터 데이터베이스와 호환되는 모델 사용
            self.local_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ 로컬 임베딩 모델 초기화 완료 (all-MiniLM-L6-v2)")
            
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
            # 텍스트 전처리
            processed_texts = [self._preprocess_text(text) for text in texts]
            
            embeddings = self.local_model.encode(
                processed_texts,
                convert_to_tensor=False,
                normalize_embeddings=True  # 코사인 유사도 최적화
            )
            return embeddings.tolist()
            
        except Exception as e:
            print(f"❌ 로컬 임베딩 생성 실패: {e}")
            raise
    
    def _preprocess_text(self, text: str) -> str:
        """텍스트 전처리"""
        # 불필요한 공백 제거
        text = ' '.join(text.split())
        # 특수문자 정리
        text = text.strip()
        return text
    
    def get_single_embedding(self, text: str) -> List[float]:
        """단일 텍스트에 대한 임베딩 생성"""
        embeddings = self.get_embeddings([text])
        return embeddings[0] if embeddings else []
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """두 임베딩 간의 코사인 유사도 계산"""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # 정규화
            vec1_norm = vec1 / np.linalg.norm(vec1)
            vec2_norm = vec2 / np.linalg.norm(vec2)
            
            # 코사인 유사도 계산
            similarity = np.dot(vec1_norm, vec2_norm)
            return float(similarity)
            
        except Exception as e:
            print(f"❌ 유사도 계산 실패: {e}")
            return 0.0


# 전역 임베딩 서비스 인스턴스
embedding_service = EmbeddingService() 