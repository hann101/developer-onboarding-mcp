import os
import glob
from typing import List, Dict, Any
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader
)
from app.core.config import settings


class DocumentLoader:
    """문서 로더 및 청킹 서비스"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.max_chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_documents_from_directory(self, directory: str = "") -> List[Dict[str, Any]]:
        """디렉토리에서 모든 문서를 로드하고 청킹"""
        if not directory:
            directory = settings.documents_dir
        
        documents = []
        
        # 지원하는 파일 확장자
        file_patterns = {
            "*.pdf": PyPDFLoader,
            "*.txt": TextLoader,
            "*.md": TextLoader,
            "*.docx": Docx2txtLoader
        }
        
        for pattern, loader_class in file_patterns.items():
            file_paths = glob.glob(os.path.join(directory, pattern))
            
            for file_path in file_paths:
                try:
                    print(f"📄 문서 로딩 중: {file_path}")
                    
                    # 문서 로드
                    loader = loader_class(file_path)
                    raw_docs = loader.load()
                    
                    # 청킹
                    chunks = self.text_splitter.split_documents(raw_docs)
                    
                    # 메타데이터 추가
                    for i, chunk in enumerate(chunks):
                        chunk.metadata.update({
                            "source_file": os.path.basename(file_path),
                            "file_path": file_path,
                            "chunk_index": i,
                            "total_chunks": len(chunks)
                        })
                    
                    documents.extend(chunks)
                    print(f"✅ {file_path}: {len(chunks)}개 청크 생성")
                    
                except Exception as e:
                    print(f"❌ {file_path} 로딩 실패: {e}")
                    continue
        
        print(f"📊 총 {len(documents)}개 문서 청크 로드 완료")
        return documents
    
    def load_confluence_documents(self, space_key: str, username: str, api_token: str) -> List[Dict[str, Any]]:
        """Confluence에서 문서 로드 (향후 구현)"""
        # TODO: Confluence API 연동 구현
        print("🔄 Confluence 연동 기능은 향후 구현 예정입니다.")
        return []
    
    def get_document_info(self, directory: str = "") -> Dict[str, Any]:
        """문서 디렉토리 정보 조회"""
        if not directory:
            directory = settings.documents_dir
        
        if not os.path.exists(directory):
            return {"error": f"디렉토리가 존재하지 않습니다: {directory}"}
        
        file_info = {}
        total_files = 0
        
        for file_path in glob.glob(os.path.join(directory, "*.*")):
            if file_path.lower().endswith(('.pdf', '.txt', '.md', '.docx')):
                file_size = os.path.getsize(file_path)
                file_info[os.path.basename(file_path)] = {
                    "size": file_size,
                    "path": file_path
                }
                total_files += 1
        
        return {
            "directory": directory,
            "total_files": total_files,
            "files": file_info
        }


# 전역 문서 로더 인스턴스
document_loader = DocumentLoader() 