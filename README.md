# 개발자를 위한 맞춤형 Q&A 페이지 (MCP) - Gemini 전용

RAG(Retrieval-Augmented Generation) 기반의 기술 문서 Q&A 시스템입니다.

## 주요 기능

- 📚 다양한 문서 형식 지원 (PDF, TXT, DOCX, Markdown)
- 🔍 의미 기반 문서 검색
- 🤖 Google Gemini 기반 정확한 답변 생성
- 🌐 웹 기반 사용자 인터페이스
- 📊 답변 출처 추적

## 기술 스택

- **백엔드**: Python + FastAPI
- **문서 처리**: LangChain
- **벡터 데이터베이스**: ChromaDB
- **임베딩**: sentence-transformers (로컬)
- **LLM**: Google Gemini Pro
- **프론트엔드**: HTML + JavaScript

## 설치 및 실행

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

2. 환경 변수 설정:
```bash
cp env.example .env
# .env 파일에 Google API 키를 설정하세요
```

3. 서버 실행:
```bash
python run.py
```

4. 웹 인터페이스 접속:
```
http://localhost:8000
```

## 프로젝트 구조

```
├── app/
│   ├── main.py              # FastAPI 애플리케이션
│   ├── core/
│   │   ├── config.py        # 설정 관리
│   │   └── database.py      # 벡터 데이터베이스 연결
│   ├── services/
│   │   ├── document_loader.py    # 문서 로더
│   │   ├── embedding_service.py  # 임베딩 서비스
│   │   ├── search_service.py     # 검색 서비스
│   │   └── llm_service.py        # LLM 서비스 (Gemini)
│   ├── models/
│   │   └── schemas.py       # Pydantic 모델
│   └── api/
│       └── routes.py        # API 라우트
├── documents/               # 문서 저장소
├── frontend/               # 웹 인터페이스
└── requirements.txt
```

## 환경 설정

### 필수 설정
- `GOOGLE_API_KEY`: Google Gemini API 키

### 선택 설정
- `CHROMA_PERSIST_DIRECTORY`: 벡터 DB 저장 경로 (기본: ./chroma_db)
- `DOCUMENTS_DIR`: 문서 저장 경로 (기본: ./documents)
- `HOST`: 서버 호스트 (기본: 0.0.0.0)
- `PORT`: 서버 포트 (기본: 8000)

## 사용법

1. **문서 추가**: `documents/` 폴더에 PDF, TXT, MD, DOCX 파일을 추가
2. **문서 업로드**: 웹 인터페이스에서 "문서 업로드" 버튼 클릭
3. **질문하기**: 질문을 입력하고 답변 받기

## API 엔드포인트

- `GET /api/v1/health`: 시스템 상태 확인
- `POST /api/v1/upload-documents`: 문서 업로드 및 벡터화
- `POST /api/v1/ask`: 질문에 대한 답변 생성
- `GET /api/v1/documents/info`: 문서 정보 조회
- `GET /api/v1/search/statistics`: 검색 통계 정보

## 비용 정보

- **Google Gemini Pro**: $0.001/1K input tokens, $0.002/1K output tokens
- **임베딩**: sentence-transformers (무료, 로컬)
- **벡터 DB**: ChromaDB (무료, 로컬)

## 장점

- ✅ 비용 효율적 (OpenAI 대비 매우 저렴)
- ✅ 안정적인 성능
- ✅ 로컬 임베딩으로 API 비용 절약
- ✅ 간단한 설정
- ✅ 빠른 응답 속도 