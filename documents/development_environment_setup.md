# 개발 환경 설정 가이드

## 개요
이 문서는 MSA 기반 DDD 프로젝트의 개발 환경을 설정하는 방법을 설명합니다.

## 필수 요구사항

### 1. Java 개발 환경
- **Java Version**: OpenJDK 17 LTS
- **Build Tool**: Maven 3.8+ 또는 Gradle 7.6+
- **IDE**: IntelliJ IDEA (권장) 또는 Eclipse

### 2. 데이터베이스
- **MySQL**: 8.0+
- **Redis**: 7.0+ (캐싱 및 세션 저장용)

### 3. 개발 도구
- **Git**: 2.30+
- **Docker**: 20.10+ (로컬 개발용)
- **Docker Compose**: 2.0+

## 환경 설정 단계

### 1. Java 설치
```bash
# macOS (Homebrew)
brew install openjdk@17

# Ubuntu/Debian
sudo apt update
sudo apt install openjdk-17-jdk

# Windows
# Oracle JDK 17 또는 OpenJDK 17 다운로드 후 설치
```

### 2. Maven 설치
```bash
# macOS
brew install maven

# Ubuntu/Debian
sudo apt install maven

# Windows
# Apache Maven 공식 사이트에서 다운로드
```

### 3. MySQL 설치
```bash
# macOS
brew install mysql

# Ubuntu/Debian
sudo apt install mysql-server

# Docker 사용 (권장)
docker run --name mysql-dev -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=msa_dev -p 3306:3306 -d mysql:8.0
```

### 4. Redis 설치
```bash
# macOS
brew install redis

# Ubuntu/Debian
sudo apt install redis-server

# Docker 사용
docker run --name redis-dev -p 6379:6379 -d redis:7.0
```

## 프로젝트 구조

```
msa-project/
├── member-service/          # 회원 서비스
├── shop-service/           # 상점 서비스
├── order-service/          # 주문 서비스
├── operation-service/      # 운영 서비스
├── settlement-service/     # 정산 서비스
├── api-gateway/           # API 게이트웨이
├── discovery-service/     # 서비스 디스커버리
├── config-service/        # 설정 서비스
└── shared/               # 공통 모듈
```

## 로컬 개발 환경 실행

### 1. Docker Compose로 인프라 실행
```bash
# 프로젝트 루트에서
docker-compose -f docker-compose-dev.yml up -d
```

### 2. 각 서비스 실행
```bash
# Member Service
cd member-service
./mvnw spring-boot:run

# Shop Service
cd shop-service
./mvnw spring-boot:run

# Order Service
cd order-service
./mvnw spring-boot:run

# Operation Service
cd operation-service
./mvnw spring-boot:run

# Settlement Service
cd settlement-service
./mvnw spring-boot:run
```

## 개발 포트 설정

| 서비스 | 포트 | 설명 |
|--------|------|------|
| API Gateway | 8080 | 외부 API 진입점 |
| Discovery Service | 8761 | 서비스 디스커버리 |
| Config Service | 8888 | 설정 관리 |
| Member Service | 8081 | 회원 관리 |
| Shop Service | 8082 | 상점 관리 |
| Order Service | 8083 | 주문 관리 |
| Operation Service | 8084 | 운영 관리 |
| Settlement Service | 8085 | 정산 관리 |
| MySQL | 3306 | 데이터베이스 |
| Redis | 6379 | 캐시/세션 |

## IDE 설정

### IntelliJ IDEA 설정
1. **Project Structure** → **Project Settings** → **Project**
   - Project SDK: OpenJDK 17
   - Language Level: 17

2. **Build Tools** → **Maven**
   - Maven home path 설정
   - User settings file 설정

3. **Plugins 설치**
   - Spring Boot
   - Docker
   - Database Tools
   - Git Integration

### 코드 스타일 설정
1. **Settings** → **Editor** → **Code Style**
   - Java 탭에서 프로젝트 코드 스타일 적용
   - Import Optimizer 설정

## 환경 변수 설정

### application-dev.yml 예시
```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/member_dev?useSSL=false&serverTimezone=UTC
    username: root
    password: password
    driver-class-name: com.mysql.cj.jdbc.Driver
  
  redis:
    host: localhost
    port: 6379
    
  cloud:
    config:
      uri: http://localhost:8888
    discovery:
      enabled: true
      service-id: member-service

server:
  port: 8081

logging:
  level:
    com.msa: DEBUG
    org.springframework.cloud: DEBUG
```

## 문제 해결

### 일반적인 문제들
1. **포트 충돌**: 다른 프로세스가 사용 중인 포트 확인
2. **데이터베이스 연결 실패**: MySQL 서비스 상태 확인
3. **Redis 연결 실패**: Redis 서비스 상태 확인
4. **메모리 부족**: JVM 힙 메모리 설정 조정

### 로그 확인
```bash
# 각 서비스의 로그 확인
tail -f logs/application.log

# Docker 컨테이너 로그 확인
docker logs mysql-dev
docker logs redis-dev
```

## 다음 단계
환경 설정이 완료되면 다음 문서들을 참조하세요:
- [코드 컨벤션 가이드](./coding_conventions.md)
- [DDD 설계 가이드](./ddd_design_guide.md)
- [MSA 아키텍처 가이드](./msa_architecture_guide.md) 