# 코드 컨벤션 가이드

## 개요
이 문서는 MSA 기반 DDD 프로젝트의 Java Spring Boot 코드 컨벤션을 정의합니다.

## 1. Java 코딩 컨벤션

### 1.1 명명 규칙

#### 클래스명
```java
// ✅ 올바른 예시
public class MemberService {}
public class OrderRepository {}
public class UserRegistrationEvent {}

// ❌ 잘못된 예시
public class memberService {}
public class order_repository {}
public class userRegistrationEvent {}
```

#### 메서드명
```java
// ✅ 올바른 예시
public void createMember(MemberRequest request) {}
public Member findById(Long id) {}
public boolean isValidEmail(String email) {}

// ❌ 잘못된 예시
public void CreateMember(MemberRequest request) {}
public Member find_by_id(Long id) {}
public boolean is_valid_email(String email) {}
```

#### 변수명
```java
// ✅ 올바른 예시
private String memberName;
private List<Order> orderList;
private boolean isActive;

// ❌ 잘못된 예시
private String member_name;
private List<Order> order_list;
private boolean is_active;
```

#### 상수명
```java
// ✅ 올바른 예시
public static final String DEFAULT_CURRENCY = "KRW";
public static final int MAX_RETRY_COUNT = 3;

// ❌ 잘못된 예시
public static final String default_currency = "KRW";
public static final int maxRetryCount = 3;
```

### 1.2 패키지 구조

```
com.msa.{domain}.{service}
├── application/          # 애플리케이션 서비스
│   ├── dto/             # 데이터 전송 객체
│   ├── service/         # 애플리케이션 서비스
│   └── event/           # 이벤트 핸들러
├── domain/              # 도메인 계층
│   ├── entity/          # 엔티티
│   ├── repository/      # 리포지토리 인터페이스
│   ├── service/         # 도메인 서비스
│   ├── valueobject/     # 값 객체
│   └── event/           # 도메인 이벤트
├── infrastructure/      # 인프라스트럭처 계층
│   ├── config/          # 설정
│   ├── persistence/     # 영속성 구현
│   ├── external/        # 외부 서비스 연동
│   └── messaging/       # 메시징
└── presentation/        # 프레젠테이션 계층
    ├── controller/      # 컨트롤러
    ├── dto/             # 요청/응답 DTO
    └── exception/       # 예외 처리
```

### 1.3 코드 포맷팅

#### 들여쓰기
- 탭 대신 스페이스 4개 사용
- 최대 라인 길이: 120자

#### 빈 줄 사용
```java
// ✅ 올바른 예시
@Service
@Transactional
public class MemberService {
    
    private final MemberRepository memberRepository;
    private final MemberEventPublisher eventPublisher;
    
    public MemberService(MemberRepository memberRepository, 
                        MemberEventPublisher eventPublisher) {
        this.memberRepository = memberRepository;
        this.eventPublisher = eventPublisher;
    }
    
    public Member createMember(CreateMemberRequest request) {
        // 비즈니스 로직
        Member member = Member.create(request.getName(), request.getEmail());
        
        // 저장
        Member savedMember = memberRepository.save(member);
        
        // 이벤트 발행
        eventPublisher.publish(new MemberCreatedEvent(savedMember.getId()));
        
        return savedMember;
    }
}
```

## 2. Spring Boot 컨벤션

### 2.1 의존성 주입

#### 생성자 주입 (권장)
```java
// ✅ 올바른 예시
@Service
@Transactional
public class MemberService {
    
    private final MemberRepository memberRepository;
    private final MemberEventPublisher eventPublisher;
    
    public MemberService(MemberRepository memberRepository,
                        MemberEventPublisher eventPublisher) {
        this.memberRepository = memberRepository;
        this.eventPublisher = eventPublisher;
    }
}

### 2.2 어노테이션 사용

#### 클래스 레벨 어노테이션
```java
// ✅ 올바른 예시
@RestController
@RequestMapping("/api/v1/members")
@Validated
@Slf4j
public class MemberController {
    // ...
}

@Service
@Transactional(readOnly = true)
public class MemberService {
    // ...
}

@Repository
public interface MemberRepository extends JpaRepository<Member, Long> {
    // ...
}
```

#### 메서드 레벨 어노테이션
```java
// ✅ 올바른 예시
@PostMapping
@ResponseStatus(HttpStatus.CREATED)
public ResponseEntity<MemberResponse> createMember(
        @Valid @RequestBody CreateMemberRequest request) {
    // ...
}

@GetMapping("/{id}")
public ResponseEntity<MemberResponse> getMember(@PathVariable Long id) {
    // ...
}

@Transactional
public Member createMember(CreateMemberRequest request) {
    // ...
}
```

### 2.3 예외 처리

#### 커스텀 예외 정의
```java
// ✅ 올바른 예시
public class MemberNotFoundException extends RuntimeException {
    
    public MemberNotFoundException(Long memberId) {
        super(String.format("Member not found with id: %d", memberId));
    }
}

public class InvalidEmailException extends RuntimeException {
    
    public InvalidEmailException(String email) {
        super(String.format("Invalid email format: %s", email));
    }
}
```

#### 글로벌 예외 처리
```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {
    
    @ExceptionHandler(MemberNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleMemberNotFound(
            MemberNotFoundException e) {
        log.error("Member not found: {}", e.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(new ErrorResponse("MEMBER_NOT_FOUND", e.getMessage()));
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationError(
            MethodArgumentNotValidException e) {
        log.error("Validation error: {}", e.getMessage());
        return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(new ErrorResponse("VALIDATION_ERROR", "Invalid request data"));
    }
}
```

## 3. DDD 컨벤션

### 3.1 엔티티 정의

```java
@Entity
@Table(name = "members")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Member extends BaseEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Embedded
    private MemberName name;
    
    @Embedded
    private Email email;
    
    @Enumerated(EnumType.STRING)
    private MemberStatus status;
    
    @OneToMany(mappedBy = "member", cascade = CascadeType.ALL)
    private List<MemberAddress> addresses = new ArrayList<>();
    
    // 팩토리 메서드
    public static Member create(MemberName name, Email email) {
        return new Member(name, email, MemberStatus.ACTIVE);
    }
    
    // 비즈니스 메서드
    public void updateName(MemberName newName) {
        this.name = newName;
    }
    
    public void deactivate() {
        this.status = MemberStatus.INACTIVE;
    }
    
    public boolean isActive() {
        return this.status == MemberStatus.ACTIVE;
    }
    
    // 생성자
    private Member(MemberName name, Email email, MemberStatus status) {
        this.name = name;
        this.email = email;
        this.status = status;
    }
}
```

### 3.2 값 객체 정의

```java
@Embeddable
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Email {
    
    @Column(name = "email", unique = true)
    private String value;
    
    public Email(String value) {
        validateEmail(value);
        this.value = value;
    }
    
    private void validateEmail(String email) {
        if (email == null || email.trim().isEmpty()) {
            throw new IllegalArgumentException("Email cannot be null or empty");
        }
        
        String emailRegex = "^[A-Za-z0-9+_.-]+@(.+)$";
        if (!email.matches(emailRegex)) {
            throw new IllegalArgumentException("Invalid email format");
        }
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Email email = (Email) o;
        return Objects.equals(value, email.value);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(value);
    }
}
```

### 3.3 리포지토리 인터페이스

```java
@Repository
public interface MemberRepository extends JpaRepository<Member, Long> {
    
    Optional<Member> findByEmail(Email email);
    
    List<Member> findByStatus(MemberStatus status);
    
    @Query("SELECT m FROM Member m WHERE m.createdAt >= :startDate")
    List<Member> findMembersCreatedAfter(@Param("startDate") LocalDateTime startDate);
    
    boolean existsByEmail(Email email);
}
```

## 4. API 설계 컨벤션

### 4.1 REST API 설계

#### URL 구조
```
GET    /api/v1/members          # 회원 목록 조회
GET    /api/v1/members/{id}     # 회원 상세 조회
POST   /api/v1/members          # 회원 생성
PUT    /api/v1/members/{id}     # 회원 수정
DELETE /api/v1/members/{id}     # 회원 삭제
```

#### HTTP 상태 코드
```java
// ✅ 올바른 예시
@PostMapping
@ResponseStatus(HttpStatus.CREATED)
public ResponseEntity<MemberResponse> createMember(...) {
    // 201 Created
}

@GetMapping("/{id}")
public ResponseEntity<MemberResponse> getMember(@PathVariable Long id) {
    // 200 OK 또는 404 Not Found
}

@PutMapping("/{id}")
public ResponseEntity<MemberResponse> updateMember(...) {
    // 200 OK 또는 404 Not Found
}

@DeleteMapping("/{id}")
@ResponseStatus(HttpStatus.NO_CONTENT)
public ResponseEntity<Void> deleteMember(@PathVariable Long id) {
    // 204 No Content
}
```

### 4.2 DTO 설계

#### 요청 DTO
```java
@Getter
@NoArgsConstructor
public class CreateMemberRequest {
    
    @NotBlank(message = "이름은 필수입니다")
    @Size(min = 2, max = 50, message = "이름은 2-50자 사이여야 합니다")
    private String name;
    
    @NotBlank(message = "이메일은 필수입니다")
    @Email(message = "올바른 이메일 형식이 아닙니다")
    private String email;
    
    @NotBlank(message = "비밀번호는 필수입니다")
    @Size(min = 8, message = "비밀번호는 최소 8자 이상이어야 합니다")
    private String password;
}
```

#### 응답 DTO
```java
@Getter
@Builder
public class MemberResponse {
    
    private Long id;
    private String name;
    private String email;
    private String status;
    private LocalDateTime createdAt;
    
    public static MemberResponse from(Member member) {
        return MemberResponse.builder()
                .id(member.getId())
                .name(member.getName().getValue())
                .email(member.getEmail().getValue())
                .status(member.getStatus().name())
                .createdAt(member.getCreatedAt())
                .build();
    }
}
```

## 5. 테스트 컨벤션

### 5.1 단위 테스트

```java
@ExtendWith(MockitoExtension.class)
class MemberServiceTest {
    
    @Mock
    private MemberRepository memberRepository;
    
    @Mock
    private MemberEventPublisher eventPublisher;
    
    @InjectMocks
    private MemberService memberService;
    
    @Test
    @DisplayName("회원 생성 성공")
    void createMember_Success() {
        // Given
        CreateMemberRequest request = new CreateMemberRequest("홍길동", "hong@example.com");
        Member savedMember = Member.create(new MemberName("홍길동"), new Email("hong@example.com"));
        
        when(memberRepository.save(any(Member.class))).thenReturn(savedMember);
        
        // When
        Member result = memberService.createMember(request);
        
        // Then
        assertThat(result).isNotNull();
        assertThat(result.getName().getValue()).isEqualTo("홍길동");
        verify(eventPublisher).publish(any(MemberCreatedEvent.class));
    }
    
    @Test
    @DisplayName("중복 이메일로 회원 생성 실패")
    void createMember_DuplicateEmail_ThrowsException() {
        // Given
        CreateMemberRequest request = new CreateMemberRequest("홍길동", "hong@example.com");
        when(memberRepository.existsByEmail(any(Email.class))).thenReturn(true);
        
        // When & Then
        assertThatThrownBy(() -> memberService.createMember(request))
                .isInstanceOf(DuplicateEmailException.class);
    }
}
```

### 5.2 통합 테스트

```java
@SpringBootTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Transactional
class MemberControllerIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Autowired
    private MemberRepository memberRepository;
    
    @Test
    @DisplayName("회원 생성 API 테스트")
    void createMember_Success() {
        // Given
        CreateMemberRequest request = new CreateMemberRequest("홍길동", "hong@example.com");
        
        // When
        ResponseEntity<MemberResponse> response = restTemplate.postForEntity(
                "/api/v1/members", request, MemberResponse.class);
        
        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody()).isNotNull();
        assertThat(response.getBody().getName()).isEqualTo("홍길동");
    }
}
```

## 6. 로깅 컨벤션

### 6.1 로그 레벨 사용

```java
@Slf4j
@Service
public class MemberService {
    
    public Member createMember(CreateMemberRequest request) {
        log.info("Creating member with email: {}", request.getEmail());
        
        try {
            Member member = Member.create(new MemberName(request.getName()), 
                                        new Email(request.getEmail()));
            Member savedMember = memberRepository.save(member);
            
            log.info("Member created successfully with id: {}", savedMember.getId());
            return savedMember;
            
        } catch (Exception e) {
            log.error("Failed to create member with email: {}", request.getEmail(), e);
            throw e;
        }
    }
}
```

### 6.2 로그 포맷

```yaml
# application.yml
logging:
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
    file: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
  level:
    com.msa: INFO
    org.springframework.web: DEBUG
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE
```

## 7. 성능 최적화 컨벤션

### 7.1 N+1 문제 해결

```java
// ❌ 잘못된 예시
@Query("SELECT m FROM Member m")
List<Member> findAllMembers();

// ✅ 올바른 예시
@Query("SELECT DISTINCT m FROM Member m LEFT JOIN FETCH m.addresses")
List<Member> findAllMembersWithAddresses();
```

### 7.2 캐싱 사용

```java
@Service
@CacheConfig(cacheNames = "members")
public class MemberService {
    
    @Cacheable(key = "#id")
    public Member findById(Long id) {
        return memberRepository.findById(id)
                .orElseThrow(() -> new MemberNotFoundException(id));
    }
    
    @CacheEvict(key = "#member.id")
    public Member updateMember(Member member) {
        return memberRepository.save(member);
    }
}
```

## 8. 보안 컨벤션

### 8.1 입력 검증

```java
@RestController
@Validated
public class MemberController {
    
    @PostMapping
    public ResponseEntity<MemberResponse> createMember(
            @Valid @RequestBody CreateMemberRequest request) {
        // 검증된 요청 처리
    }
}
```

### 8.2 SQL 인젝션 방지

```java
// ✅ 올바른 예시 (JPA 사용)
@Query("SELECT m FROM Member m WHERE m.email = :email")
Optional<Member> findByEmail(@Param("email") Email email);

// ❌ 잘못된 예시 (문자열 연결)
@Query("SELECT m FROM Member m WHERE m.email = '" + email + "'")
Optional<Member> findByEmail(String email);
```

이 컨벤션을 따르면 일관성 있고 유지보수하기 쉬운 코드를 작성할 수 있습니다. 