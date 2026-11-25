# Refine AI

**짧은 요청을 용도에 맞는 프롬프트로 다듬는 웹 서비스**  
디자인적사고 최종 과제 · 2025년 12월 · 이혁수 개인 개발

“사이버펑크 스타일의 미래 도시 야경을 만들고 싶다”는 생각을 이미지 도구에 어떻게 설명하면 좋을까? Refine AI에 요청을 적고 분야와 문체를 고르면, GPT-4o가 입력에서 빠진 맥락과 출력 형식을 살펴보고 영문 프롬프트를 제안합니다. 입력·결과 화면, FastAPI 서버, 모델 호출, SQLite 기록 조회까지 직접 개발했습니다.

## 사용 예시

| 단계 | 이미지 프롬프트를 다듬을 때 |
| --- | --- |
| 요청 입력 | “사이버펑크 스타일의 미래 도시 야경 프롬프트 작성해줘”를 입력하고 문체는 `Creative`, 분야는 `Image`로 선택합니다. |
| 프롬프트 개선 | 서버가 요청과 스타일을 GPT-4o에 보냅니다. 이미지 용도에는 카메라 구도, 조명, 장면의 세부 묘사를 담은 지시문을 작성하도록 합니다. |
| 결과 사용 | 화면에서 개선된 영문 프롬프트와 작성 팁을 확인하고, 복사해서 원하는 창작 도구에 붙여 넣습니다. |
| 기록 확인 | **내 정보**에서 원문과 개선문을 나란히 보고, 최근 20건의 기록과 분야별 사용 횟수를 확인합니다. |

코딩, 글쓰기, 수학, 데이터 분석 등 다른 용도도 선택할 수 있습니다. 분야를 자동으로 두면 모델이 요청 내용을 보고 분류합니다. [화면과 예시 입력](templates/index.html) · [용도별 프롬프트 구성](app/services/service.py#L44-L88)

## 구현

| 구성 | 구현한 기능 |
| --- | --- |
| FastAPI · Jinja2 | 요청 입력, 결과 복사, 이력 조회 화면을 제공하고, 입력 문장·문체·분야를 `POST /api/refine`으로 받습니다. |
| OpenAI Chat Completions · Pydantic | 시스템 지시와 사용자 입력을 나눠 전송합니다. JSON 응답에서 개선문, 분류, 맥락·출력 형식의 누락 여부, 제안과 팁을 읽어 응답 모델로 구성합니다. |
| SQLAlchemy · SQLite | `prompt_history` 테이블에 원문, 개선문, 분야, 두 누락 여부와 생성 시각을 저장합니다. 전체 기록은 최신순으로 조회하고 분야별 횟수는 `GROUP BY`로 집계합니다. |

실제 프롬프트 개선 요청을 처리하는 모델은 `gpt-4o`입니다. 메인 화면의 ChatGPT·Gemini·Grok 버튼은 결과를 활용할 외부 서비스로 이동하는 링크입니다. [모델 호출](app/services/service.py#L92-L113) · [기록 모델](app/models/models.py#L5-L17) · [저장과 집계](app/routers/prompt.py#L15-L55)

## 로컬 실행

Python 3.12와 Poetry가 필요합니다. 아래 명령은 저장소 루트에서 실행합니다. 앱을 시작하면 현재 폴더에 SQLite 파일 `prompt_refiner.db`와 테이블이 만들어집니다.

### 1. 환경 준비

```bash
git clone https://github.com/leehyeoksu/fastapi.git
cd fastapi
poetry install --no-root
```

Poetry는 [poetry.lock](poetry.lock)에 기록된 버전으로 FastAPI, OpenAI SDK, SQLAlchemy와 화면 렌더링에 필요한 Jinja2를 설치합니다.

### 2. 키 설정

저장소 루트에 `config.json`을 만듭니다. 화면, 저장, 통계를 먼저 확인하려면 아래 값을 그대로 사용하세요. `your-`로 시작하는 값은 앱이 인식하는 시연용 설정입니다. 이때는 외부 API 호출 없이 키 설정을 안내하는 응답이 저장됩니다.

```json
{
  "OPENAI_API_KEY": "your-demo-key"
}
```

실제로 프롬프트를 생성하려면 `your-demo-key`를 GPT-4o 호출 권한이 있는 본인의 OpenAI API 키로 바꿉니다. 앱은 요청할 때마다 이 파일을 읽습니다. `config.json`과 DB 파일은 `.gitignore`에 포함되어 있습니다.

### 3. 서버 시작

```bash
poetry run python -m uvicorn main:app --reload
```

[입력 화면](http://127.0.0.1:8000/)에서 요청을 한 건 보낸 뒤 [기록·통계](http://127.0.0.1:8000/my-info)에서 저장 결과를 확인하세요. [자동 생성된 API 문서](http://127.0.0.1:8000/docs)에서도 같은 요청을 보낼 수 있습니다.

## API

| 메서드 | 경로 | 기능 |
| --- | --- | --- |
| `POST` | `/api/refine` | 프롬프트 개선·분석 후 원문과 결과 저장 |
| `GET` | `/api/history?skip=0&limit=10` | 최신 기록부터 페이지 단위로 조회 |
| `GET` | `/api/stats` | 분야별 기록 수 조회 |
| `DELETE` | `/api/history/{history_id}` | 지정한 기록 한 건 삭제 |
| `DELETE` | `/api/history` | 현재 SQLite DB의 전체 기록 삭제 |

`POST /api/refine` 요청 예시

```json
{
  "prompt": "사이버펑크 스타일의 미래 도시 야경 프롬프트 작성해줘.",
  "style": "Creative",
  "category": "Image"
}
```

응답의 `original_prompt`와 `refined_prompt`로 원문과 개선문을 비교합니다. `analysis`에는 분야·누락 여부·개선 제안이, `tips`에는 작성 팁이 담깁니다. 현재 이력과 통계는 실행 중인 앱의 SQLite DB를 공유합니다. [요청·응답 스키마](app/schemas/schemas.py#L5-L32)

설계와 학습 과정을 더 보려면 [프로젝트 학습 기록](README_STUDY.md)을 참고하세요.
