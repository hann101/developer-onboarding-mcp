from typing import List, Dict, Any
from app.core.database import vector_db
from app.services.embedding_service import embedding_service


class SearchService:
    """검색 서비스"""
    
    def __init__(self):
        self.vector_db = vector_db
        self.embedding_service = embedding_service
    
    def search_documents(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """질문에 대한 관련 문서 검색"""
        try:
            # 질문을 임베딩으로 변환
            query_embedding = self.embedding_service.get_single_embedding(query)
            
            if not query_embedding:
                raise ValueError("질문 임베딩 생성에 실패했습니다.")
            
            # 벡터 데이터베이스에서 유사한 문서 검색
            search_results = self.vector_db.search(
                query_embedding=query_embedding,
                n_results=max_results
            )
            
            # 결과 포맷팅
            formatted_results = []
            if search_results and 'documents' in search_results:
                documents = search_results['documents'][0]
                metadatas = search_results.get('metadatas', [[]])[0]
                distances = search_results.get('distances', [[]])[0]
                
                for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
                    formatted_results.append({
                        "content": doc,
                        "metadata": metadata or {},
                        "distance": distance,
                        "relevance_score": 1 - distance  # 거리를 관련성 점수로 변환
                    })
            
            print(f"🔍 '{query}'에 대한 {len(formatted_results)}개 관련 문서 검색 완료")
            return formatted_results
            
        except Exception as e:
            print(f"❌ 문서 검색 실패: {e}")
            raise
    
    def get_most_relevant_chunks(self, query: str, max_results: int = 3) -> List[str]:
        """가장 관련성 높은 문서 청크들 반환"""
        try:
            search_results = self.search_documents(query, max_results)
            
            # 관련성 점수로 정렬
            sorted_results = sorted(
                search_results, 
                key=lambda x: x['relevance_score'], 
                reverse=True
            )
            
            # 임계값 이상의 관련성만 필터링
            relevant_chunks = [
                result['content'] for result in sorted_results
                if result['relevance_score'] > 0.7  # 70% 이상 관련성
            ]
            
            return relevant_chunks
            
        except Exception as e:
            print(f"❌ 관련 문서 청크 검색 실패: {e}")
            return []
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """검색 통계 정보"""
        try:
            db_info = self.vector_db.get_collection_info()
            return {
                "database_info": db_info,
                "embedding_model": "OpenAI text-embedding-ada-002 (폴백: sentence-transformers)",
                "search_algorithm": "Cosine Similarity"
            }
        except Exception as e:
            return {"error": f"통계 정보 조회 실패: {e}"}


# 전역 검색 서비스 인스턴스
search_service = SearchService() 