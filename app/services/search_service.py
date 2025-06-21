from typing import List, Dict, Any
import re
from app.core.database import vector_db
from app.services.embedding_service import embedding_service


class SearchService:
    """검색 서비스"""
    
    def __init__(self):
        self.vector_db = vector_db
        self.embedding_service = embedding_service
    
    def search_documents(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """질문에 대한 관련 문서 검색 (개선된 버전)"""
        try:
            # 질문 전처리
            processed_query = self._preprocess_query(query)
            
            # 질문을 임베딩으로 변환
            query_embedding = self.embedding_service.get_single_embedding(processed_query)
            
            if not query_embedding:
                raise ValueError("질문 임베딩 생성에 실패했습니다.")
            
            # 벡터 데이터베이스에서 유사한 문서 검색 (더 많은 결과 가져오기)
            initial_results = self.vector_db.search(
                query_embedding=query_embedding,
                n_results=min(max_results * 3, 20)  # 더 많은 후보 검색
            )
            
            # 결과 포맷팅 및 초기 점수 계산
            formatted_results = []
            if initial_results and 'documents' in initial_results:
                documents = initial_results['documents'][0]
                metadatas = initial_results.get('metadatas', [[]])[0]
                distances = initial_results.get('distances', [[]])[0]
                
                for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
                    # 키워드 매칭 점수 계산
                    keyword_score = self._calculate_keyword_score(query, doc)
                    
                    # 벡터 유사도 점수
                    vector_score = 1 - distance
                    
                    # 종합 점수 (벡터 유사도 70%, 키워드 매칭 30%)
                    combined_score = (vector_score * 0.7) + (keyword_score * 0.3)
                    
                    formatted_results.append({
                        "content": doc,
                        "metadata": metadata or {},
                        "distance": distance,
                        "vector_score": vector_score,
                        "keyword_score": keyword_score,
                        "relevance_score": combined_score
                    })
            
            # 점수로 재정렬
            formatted_results.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            # 최종 결과 필터링 및 반환
            final_results = []
            for result in formatted_results:
                # 임계값 이상의 관련성만 포함
                if result['relevance_score'] > 0.3:  # 30% 이상 관련성
                    final_results.append(result)
                    if len(final_results) >= max_results:
                        break
            
            print(f"🔍 '{query}'에 대한 {len(final_results)}개 관련 문서 검색 완료")
            return final_results
            
        except Exception as e:
            print(f"❌ 문서 검색 실패: {e}")
            raise
    
    def _preprocess_query(self, query: str) -> str:
        """질문 전처리"""
        # 불필요한 공백 제거
        query = ' '.join(query.split())
        # 특수문자 정리
        query = query.strip()
        return query
    
    def _calculate_keyword_score(self, query: str, document: str) -> float:
        """키워드 매칭 점수 계산"""
        try:
            # 질문에서 키워드 추출
            query_words = set(re.findall(r'\b\w+\b', query.lower()))
            
            # 문서에서 단어 추출
            doc_words = set(re.findall(r'\b\w+\b', document.lower()))
            
            if not query_words:
                return 0.0
            
            # 매칭되는 키워드 수 계산
            matches = len(query_words.intersection(doc_words))
            
            # 점수 계산 (매칭 비율)
            score = matches / len(query_words)
            
            return min(score, 1.0)  # 최대 1.0
            
        except Exception as e:
            print(f"❌ 키워드 점수 계산 실패: {e}")
            return 0.0
    
    def get_most_relevant_chunks(self, query: str, max_results: int = 3) -> List[str]:
        """가장 관련성 높은 문서 청크들 반환 (개선된 버전)"""
        try:
            search_results = self.search_documents(query, max_results * 2)
            
            # 관련성 점수로 정렬
            sorted_results = sorted(
                search_results, 
                key=lambda x: x['relevance_score'], 
                reverse=True
            )
            
            # 더 엄격한 임계값 적용
            relevant_chunks = [
                result['content'] for result in sorted_results
                if result['relevance_score'] > 0.5  # 50% 이상 관련성
            ]
            
            # 최대 결과 수 제한
            return relevant_chunks[:max_results]
            
        except Exception as e:
            print(f"❌ 관련 문서 청크 검색 실패: {e}")
            return []
    
    def search_by_keywords(self, keywords: List[str], max_results: int = 5) -> List[Dict[str, Any]]:
        """키워드 기반 검색"""
        try:
            # 키워드를 하나의 쿼리로 결합
            query = ' '.join(keywords)
            return self.search_documents(query, max_results)
            
        except Exception as e:
            print(f"❌ 키워드 검색 실패: {e}")
            return []
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """검색 통계 정보"""
        try:
            db_info = self.vector_db.get_collection_info()
            return {
                "database_info": db_info,
                "embedding_model": "all-MiniLM-L6-v2",
                "search_algorithm": "Hybrid Search (Vector + Keyword)",
                "search_features": [
                    "벡터 유사도 검색",
                    "키워드 매칭",
                    "재순위화",
                    "임계값 필터링"
                ]
            }
        except Exception as e:
            return {"error": f"통계 정보 조회 실패: {e}"}


# 전역 검색 서비스 인스턴스
search_service = SearchService() 