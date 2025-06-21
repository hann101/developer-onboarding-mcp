import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings
from typing import List, Dict, Any, Optional


class VectorDatabase:
    """벡터 데이터베이스 관리 클래스"""
    
    def __init__(self):
        self.client: Optional[chromadb.PersistentClient] = None
        self.collection: Optional[chromadb.Collection] = None
        self._initialize_database()
    
    def _initialize_database(self):
        """데이터베이스 초기화"""
        try:
            # ChromaDB 클라이언트 생성
            self.client = chromadb.PersistentClient(
                path=settings.chroma_persist_directory,
                settings=ChromaSettings(
                    anonymized_telemetry=False
                )
            )
            
            # 컬렉션 생성 또는 가져오기
            self.collection = self.client.get_or_create_collection(
                name="developer_docs",
                metadata={"description": "개발자 문서 벡터 저장소"}
            )
            
            print(f"✅ 벡터 데이터베이스 초기화 완료: {settings.chroma_persist_directory}")
            
        except Exception as e:
            print(f"❌ 벡터 데이터베이스 초기화 실패: {e}")
            raise
    
    def add_documents(self, documents: List[str], embeddings: List[List[float]], metadatas: Optional[List[Dict[str, Any]]] = None):
        """문서를 벡터 데이터베이스에 추가"""
        try:
            if self.collection is None:
                raise Exception("컬렉션이 초기화되지 않았습니다.")
                
            if metadatas is None:
                metadatas = [{} for _ in documents]
            
            # 고유 ID 생성
            ids = [f"doc_{i}_{hash(doc[:100])}" for i, doc in enumerate(documents)]
            
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✅ {len(documents)}개 문서가 벡터 데이터베이스에 추가되었습니다.")
            
        except Exception as e:
            print(f"❌ 문서 추가 실패: {e}")
            raise
    
    def search(self, query_embedding: List[float], n_results: int = 5):
        """유사한 문서 검색"""
        try:
            if self.collection is None:
                raise Exception("컬렉션이 초기화되지 않았습니다.")
                
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            return results
            
        except Exception as e:
            print(f"❌ 검색 실패: {e}")
            raise
    
    def get_collection_info(self) -> Dict[str, Any]:
        """컬렉션 정보 조회"""
        try:
            if self.collection is None:
                return {"error": "컬렉션이 초기화되지 않았습니다."}
                
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection.name
            }
        except Exception as e:
            print(f"❌ 컬렉션 정보 조회 실패: {e}")
            return {"error": str(e)}
    
    def get_chunks_info(self) -> Dict[str, Any]:
        """저장된 청크들의 상세 정보 조회"""
        try:
            if self.collection is None:
                return {"error": "컬렉션이 초기화되지 않았습니다."}
                
            count = self.collection.count()
            if count == 0:
                return {
                    "total_chunks": 0,
                    "chunks": [],
                    "file_distribution": {}
                }
            
            # 모든 문서 조회
            results = self.collection.get(
                include=["documents", "metadatas"]
            )
            
            if results is None or 'documents' not in results:
                return {"error": "문서 조회 결과가 없습니다."}
            
            chunks = []
            file_distribution = {}
            
            documents = results['documents']
            metadatas = results['metadatas']
            ids = results['ids']
            
            for i in range(len(documents)):
                content = documents[i]
                metadata = metadatas[i] if i < len(metadatas) else {}
                
                # 파일별 분포 계산
                source_file = metadata.get('source_file', 'unknown')
                if source_file not in file_distribution:
                    file_distribution[source_file] = 0
                file_distribution[source_file] += 1
                
                # 청크 정보 구성
                chunk_info = {
                    "id": ids[i] if i < len(ids) else f"chunk_{i}",
                    "content_preview": content[:100] + "..." if len(content) > 100 else content,
                    "content_length": len(content),
                    "metadata": metadata
                }
                chunks.append(chunk_info)
            
            return {
                "total_chunks": count,
                "chunks": chunks,
                "file_distribution": file_distribution
            }
            
        except Exception as e:
            print(f"❌ 청크 정보 조회 실패: {e}")
            return {"error": str(e)}


# 전역 데이터베이스 인스턴스
vector_db = VectorDatabase() 