# Refine AI 코드 분석 및 발표 스크립트 (Code Walkthrough)

발표 시 실제 코드를 보여주며 설명할 때 사용할 수 있는 상세 가이드입니다. 핵심 로직 위주로 설명하세요.

---

## 1. 📂 `app/main.py` (핵심 애플리케이션 팩토리)
**역할**: FastAPI 앱을 생성하고, 전역 설정(CORS 등)을 관리하며 라우터를 등록하는 곳.

**🧑‍🏫 발표 포인트**:
- **`create_app()` 함수**: 애플리케이션 생성 로직을 함수로 감싸서 유연성을 확보했습니다 (팩토리 패턴).
- **CORS 설정**: 프론트엔드와 백엔드가 다른 도메인이어도 통신 가능하도록 `allow_origins=["*"]`로 설정했습니다.
- **라우터 통합**: `app.include_router(prompt.router)`를 통해 기능별로 쪼개진 API들을 하나로 합칩니다.

---

## 2. 📂 `app/database/database.py` (비동기 DB 연결)
**역할**: SQLite 데이터베이스와의 연결 세션(Session)을 관리.

**🧑‍🏫 발표 포인트**:
- **SQLAlchemy 엔진**: `sqlite:///./prompt_refiner.db` 파일을 사용하여 가볍고 빠르게 DB를 구축했습니다.
- **`get_db()` 의존성 주입**: API 요청이 들어올 때마다 DB 세션을 열고, 일이 끝나면 자동으로 닫아주는(`yield` -> `finally close`) 안전한 패턴을 사용했습니다.

---

## 3. 📂 `app/models/models.py` (DB 스키마)
**역할**: 데이터베이스 테이블 구조를 정의하는 설계도.

**🧑‍🏫 발표 포인트**:
- **`PromptHistory` 테이블**: 우리 서비스의 핵심인 프롬프트 이력을 저장합니다.
- **주요 컬럼**:
  - `original_prompt` vs `refined_prompt`: 개선 전후를 비교 저장.
  - `category`: AI가 분석한 질문의 유형(Coding, Writing 등).
  - `missing_context`: 'AI가 봤을 때 사용자가 뭘 빠뜨렸는지' 체크하는 진단 필드.

---

## 4. 📂 `app/schemas/schemas.py` (데이터 검증 - Pydantic)
**역할**: API로 들어오고 나가는 데이터의 형식을 엄격하게 검사.

**🧑‍🏫 발표 포인트**:
- **API와 DB의 분리**: DB 모델을 그대로 내보내지 않고, Pydantic 스키마(`PromptRequest`, `RefineResponse`)를 거쳐서 안전하게 데이터를 주고받습니다.
- **타입 힌트**: `str`, `bool` 등을 명시하여 잘못된 데이터가 들어오면 서버가 400 에러를 뱉도록 자동화했습니다.

---

## 5. 📂 `app/routers/prompt.py` (API 컨트롤러)
**역할**: 실제 클라이언트(프론트)의 요청을 받아서 서비스를 호출하는 창구.

**🧑‍🏫 발표 포인트**:
- **`POST /refine`**: 가장 핵심인 프롬프트 개선 요청을 처리합니다. DTO(`PromptRequest`)로 입력을 받고, 서비스 로직에 넘깁니다.
- **`GET /history`**: 단순 조회가 아니라, 최신순 정렬(desc) 및 빠른 조회를 담당합니다.
- **의존성 주입(`Depends`)**: `db: Session = Depends(get_db)` 코드를 통해 모든 요청에서 안전하게 DB 세션을 가져다 씁니다.

---

## 6. 📂 `app/services/service.py` (비즈니스 로직 - 핵심 AI 엔진)
**역할**: OpenAI GPT와의 통신, 프롬프트 엔지니어링, 복잡한 계산을 담당. **가장 중요한 파일!**

**🧑‍🏫 발표 포인트**:
- **시스템 프롬프트 설계**:
  > "너는 프롬프트 엔지니어링 전문가야. 사용자의 질문을 분석해서 카테고리를 분류하고, 부족한 점(Context, Format)을 채워줘."
  라는 구체적인 지시사항을 GPT에게 전달하는 로직이 여기에 있습니다.
- **JSON 모드 강제**: GPT가 말을 막 하지 않고, 우리가 원하는 `{"refined_prompt": ..., "analysis": ...}` 포맷으로만 대답하도록 `response_format={"type": "json_object"}`를 썼습니다. (신뢰성 확보)
- **에러 핸들링**: API 키가 없거나 통신이 실패했을 때 서버가 죽지 않고 적절한 메시지를 반환하도록 방어 코드를 작성했습니다.
