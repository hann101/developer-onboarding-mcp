#!/usr/bin/env python3
"""
개발자를 위한 맞춤형 Q&A 시스템 실행 스크립트
"""

import os
import sys
import uvicorn
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.config import settings


def check_environment():
    """환경 설정 확인"""
    print("🔍 환경 설정 확인 중...")
    
    # .env 파일 확인
    env_file = project_root / ".env"
    if not env_file.exists():
        print("⚠️  .env 파일이 없습니다. env.example을 복사하여 설정하세요.")
        print("   cp env.example .env")
        print("   그리고 Google API 키를 설정하세요.")
        return False
    
    # Google API 키 확인
    if not settings.google_api_key or settings.google_api_key == "your_google_api_key_here":
        print("⚠️  Google API 키가 설정되지 않았습니다.")
        print("   .env 파일에서 GOOGLE_API_KEY를 설정하세요.")
        return False
    
    print("✅ 환경 설정 확인 완료")
    return True


def create_directories():
    """필요한 디렉토리 생성"""
    print("📁 디렉토리 생성 중...")
    
    directories = [
        settings.documents_dir,
        settings.chroma_persist_directory
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")
    
    print("✅ 디렉토리 생성 완료")


def main():
    """메인 실행 함수"""
    print("🚀 개발자를 위한 맞춤형 Q&A 시스템 (Gemini 전용)")
    print("=" * 50)
    
    # 환경 설정 확인
    if not check_environment():
        print("\n❌ 환경 설정이 완료되지 않았습니다.")
        print("   위의 지시사항을 따라 설정을 완료한 후 다시 실행하세요.")
        sys.exit(1)
    
    # 디렉토리 생성
    create_directories()
    
    print("\n🌐 서버 시작 중...")
    print(f"   📚 문서 디렉토리: {settings.documents_dir}")
    print(f"   🗄️ 벡터 데이터베이스: {settings.chroma_persist_directory}")
    print(f"   🌐 서버 주소: http://{settings.host}:{settings.port}")
    print(f"   📖 API 문서: http://{settings.host}:{settings.port}/docs")
    print(f"   🖥️ 웹 인터페이스: http://{settings.host}:{settings.port}")
    print(f"   🤖 사용 모델: Google Gemini Pro")
    
    print("\n💡 사용법:")
    print("   1. documents 폴더에 PDF, TXT, MD, DOCX 파일을 추가하세요")
    print("   2. 웹 인터페이스에서 '문서 업로드' 버튼을 클릭하세요")
    print("   3. 질문을 입력하고 답변을 받아보세요")
    
    print("\n" + "=" * 50)
    
    # 서버 실행
    try:
        uvicorn.run(
            "app.main:app",
            host=settings.host,
            port=settings.port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 서버가 종료되었습니다.")
    except Exception as e:
        print(f"\n❌ 서버 실행 중 오류가 발생했습니다: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 