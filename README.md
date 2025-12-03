<<<<<<< HEAD
# fastapi
practice fastapi for projects 
=======
# 🚀 Prompt Refiner Service

AI 기반 프롬프트 분석 및 개선 서비스입니다.

## 📦 설치 및 실행 방법

### 1. 환경 설정
필요한 패키지를 설치합니다.
```bash
pip install -r requirements.txt
```

### 2. API Key 설정
`config.json` 파일을 열고 OpenAI API Key를 입력하세요.
```json
{
  "OPENAI_API_KEY": "sk-..."
}
```

### 3. 서버 실행
아래 명령어로 서버를 실행합니다.
```bash
uvicorn main:app --reload
```

### 4. 사용 방법
브라우저에서 `http://localhost:8000/docs` 로 접속하면 API를 테스트할 수 있습니다.

## 📂 파일 구조
- `main.py`: 메인 서버 파일
- `service.py`: AI 로직 처리
- `models.py`: DB 모델
- `schemas.py`: 데이터 검증 모델
- `Sprint_Process.ipynb`: 개발 과정 및 아키텍처 문서
>>>>>>> 1d9ec90 (Initial FastAPI project upload)
