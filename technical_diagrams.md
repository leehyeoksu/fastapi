# Refine AI 기술 다이어그램 (상세본)

주피터 노트북에서 바로 사용할 수 있는 상세한 Mermaid 다이어그램 코드입니다.

## 1. 전체 시스템 아키텍처 (Architecture Overview)
Refine AI 시스템의 상세 구성요소 및 데이터 흐름을 보여줍니다.

```mermaid
graph TD
    Client["사용자 브라우저 (Web Browser)"] -->|HTTP Request| Uvicorn["Uvicorn ASGI 서버"]
    Uvicorn -->|Mount| FastAPI["FastAPI 애플리케이션"]
    
    subgraph Frontend ["프론트엔드 (Jinja2 & Static)"]
        FastAPI -->|Serve| Templates["Jinja2 템플릿 (UI)"]
        FastAPI -->|Serve| Static["정적 파일 (CSS, JS, Images)"]
    end

    subgraph Backend ["백엔드 (Core Logic)"]
        FastAPI --> Router["API 라우터 (api/prompt.py)"]
        Router -->|Validation| Pydantic["Pydantic 스키마 (Schemas)"]
        Router -->|Business Logic| Service["서비스 레이어 (service.py)"]
        
        Service -->|Configuration| Config["설정 파일 (config.json)"]
        Service -->|DB Operation| SQLAlchemy["SQLAlchemy ORM"]
        SQLAlchemy -->|Query/Transaction| SQLite["SQLite 데이터베이스"]
        
        Service -->|External API| OpenAI["OpenAI GPT API"]
    end
```

## 2. API 데이터 흐름도 (API Flow Diagram)
프롬프트 개선 요청 시 데이터가 각 계층을 통과하며 변환되는 과정입니다.

```mermaid
sequenceDiagram
    participant User as 사용자
    participant Browser as 브라우저 (JS)
    participant API as API 라우터 (POST /refine)
    participant Schema as Pydantic 검증
    participant Service as 서비스 로직
    participant OpenAI as OpenAI GPT-4

    User->>Browser: 프롬프트 입력 및 스타일 선택
    Note right of User: "파이썬 코드 짜줘", "Creative"
    
    Browser->>API: JSON 요청 전송
    Note right of Browser: { "prompt": "...", "style": "...", "category": "Auto" }
    
    API->>Schema: PromptRequest 모델 검증
    Schema-->>API: 유효 데이터 확인
    
    API->>Service: process_prompt_with_ai() 호출
    
    Service->>Service: 시스템 프롬프트 구성 (Role, Constraints)
    Service->>OpenAI: Chat Completion 요청 (JSON Mode)
    OpenAI-->>Service: 구조화된 JSON 응답
    Note left of OpenAI: { "refined_prompt": "...", "analysis": {...} }
    
    Service->>API: RefineResponse 객체 반환
    API-->>Browser: 최종 JSON 응답
    Browser->>User: 결과 화면 표시
```

## 3. 데이터베이스 설계도 (ER D, Entity-Relationship Diagram)
프롬프트 히스토리 저장을 위한 `prompt_history` 테이블 상세 구조입니다.

```mermaid
erDiagram
    PROMPT_HISTORY {
        INTEGER id PK "기본키 (Auto Increment)"
        TEXT original_prompt "사용자 원본 입력 (Not Null)"
        TEXT refined_prompt "AI 개선 프롬프트 (Nullable)"
        VARCHAR category "분류 (Coding, Writing, Image 등)"
        BOOLEAN missing_context "맥락 누락 여부"
        BOOLEAN missing_format "형식 누락 여부"
        DATETIME created_at "생성 일시 (Default Now)"
    }
```

## 4. 시퀀스 다이어그램 (Sequence Diagram - 상세 처리 로직)
서비스 내부에서 일어나는 상세 처리 순서입니다.

```mermaid
sequenceDiagram
    autonumber
    actor User as 사용자
    participant UI as 웹 인터페이스
    participant Server as FastAPI 서버
    participant Service as PromptService
    participant OpenAI as GPT API
    participant DB as 데이터베이스

    User->>UI: 'Refine' 버튼 클릭
    UI->>Server: POST /api/refine
    
    rect rgb(240, 248, 255)
        note right of Server: 핵심 비즈니스 로직 시작
        Server->>Service: process_prompt_with_ai(prompt, style)
        Service->>Service: load_api_keys() (설정 로드)
        
        alt API Key 누락
            Service-->>Server: Error Response (Key Check Failed)
        else API Key 정상
            Service->>OpenAI: client.chat.completions.create()
            OpenAI-->>Service: JSON String Response
            Service->>Service: json.loads() & Parsing
            
            Service->>DB: INSERT INTO prompt_history
            DB-->>Service: Commit & Refresh (ID 생성)
        end
        
        Service-->>Server: RefineResponse 반환
    end
    
    Server-->>UI: 200 OK + JSON Data
    UI->>User: 개선된 프롬프트 & 통계 차트 업데이트
```

## 5. 프로젝트 파일 구조도 (Project File Structure)
현재 프로젝트의 실제 디렉토리 구조입니다.

```mermaid
graph LR
    %% 스타일 정의
    classDef folder fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef python fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef resource fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;
    classDef config fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;

    Root["📂 fastapi/"]:::folder
    
    subgraph Core ["핵심 애플리케이션"]
        direction TB
        App["📂 app/"]:::folder
        APIMain["🐍 main.py<br/>(앱 팩토리)"]:::python
        Routers["📂 routers/<br/>(API 경로)"]:::python
        Services["📂 services/<br/>(비즈니스 로직)"]:::python
        Models["📂 models/<br/>(DB 모델)"]:::python
        Schemas["📂 schemas/<br/>(데이터 구조)"]:::python
        Database["📂 database/<br/>(DB 연결)"]:::python
        
        App --> APIMain
        App --> Routers
        App --> Services
        App --> Models
        App --> Schemas
        App --> Database
    end
    
    subgraph Resource ["리소스"]
        direction TB
        Templates["📂 templates/<br/>(HTML 템플릿)"]:::resource
        Static["📂 static/<br/>(CSS, JS, Img)"]:::resource
    end
    
    subgraph Settings ["설정 및 실행"]
        direction TB
        Main["🐍 main.py<br/>(진입점)"]:::python
        Config["⚙️ config.json<br/>(설정)"]:::config
        DBFile["🗄️ prompt_refiner.db"]:::config
    end

    %% 연결 관계
    Root --> App
    Root --> Templates
    Root --> Static
    Root --> Main
    Root --> Config
    Root --> DBFile
```
