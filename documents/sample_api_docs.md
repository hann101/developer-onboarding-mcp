# 개발자 API 문서

## 개요
이 문서는 개발자를 위한 REST API 사용 가이드를 제공합니다.

## 인증
모든 API 요청에는 Bearer 토큰이 필요합니다.

```bash
Authorization: Bearer <your-token>
```

## 사용자 관리 API

### 사용자 목록 조회
```
GET /api/users
```

**응답 예시:**
```json
{
  "users": [
    {
      "id": 1,
      "name": "홍길동",
      "email": "hong@example.com"
    }
  ]
}
```

### 사용자 생성
```
POST /api/users
```

**요청 본문:**
```json
{
  "name": "김철수",
  "email": "kim@example.com",
  "password": "secure123"
}
```

## 에러 처리
모든 API는 표준 HTTP 상태 코드를 사용합니다:
- 200: 성공
- 400: 잘못된 요청
- 401: 인증 실패
- 404: 리소스 없음
- 500: 서버 오류

## 레이트 리미팅
API 호출은 분당 100회로 제한됩니다. 