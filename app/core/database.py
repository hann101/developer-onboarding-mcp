import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings


class VectorDatabase:
    """벡터 데이터베이스 관리 클래스"""
    
    def __init__(self):
        self.client = None
        self.collection = None
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
    
    def add_documents(self, documents: list, embeddings: list, metadatas: list = None):
        """문서를 벡터 데이터베이스에 추가"""
        try:
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
    
    def search(self, query_embedding: list, n_results: int = 5):
        """유사한 문서 검색"""
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            return results
            
        except Exception as e:
            print(f"❌ 검색 실패: {e}")
            raise
    
    def get_collection_info(self):
        """컬렉션 정보 조회"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection.name
            }
        except Exception as e:
            print(f"❌ 컬렉션 정보 조회 실패: {e}")
            return {"error": str(e)}


# 전역 데이터베이스 인스턴스
vector_db = VectorDatabase() 