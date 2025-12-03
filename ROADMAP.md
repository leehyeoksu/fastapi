# 🚀 AI 연구원을 위한 백엔드 마스터 로드맵

**목표**: FastAPI 완벽 마스터 → PyTorch AI 개발로 전환

**학습 기간**: 8-12주  
**최종 목표**: 생성형 AI 없이 독립적으로 문제 해결 & 배포까지

---

## 📍 현재 상황
- ✅ FastAPI 프로젝트 시작
- ✅ Azure MySQL 사용 중
- ✅ AWS RDS 경험 있음
- 🎯 목표: AI 연구원/엔지니어

---

## 🗺️ 학습 경로 (순서대로 읽기)

### Phase 1: 기초 다지기 (Week 1-2)

#### 📘 [01_왜_Linux인가.md](./docs/01_왜_Linux인가.md)
**학습 목표**: 백엔드 개발자가 Linux를 알아야 하는 이유
- Linux 필수 명령어 50개
- 서버 관리 자동화
- Python으로 Linux 제어

**소요 시간**: 3-4일  
**실습**: 서버 모니터링 스크립트 작성

---

#### 📘 [02_데이터베이스_선택_가이드.md](./docs/02_데이터베이스_선택_가이드.md)
**학습 목표**: 프로젝트에 맞는 DB 선택
- MySQL vs PostgreSQL vs MongoDB
- Azure Database vs AWS RDS vs Google Cloud SQL
- 현재 사용 중: Azure MySQL 완벽 활용

**소요 시간**: 2일  
**실습**: DB 비교 테스트, 성능 벤치마크

---

#### 📘 [03_FastAPI_기초.md](./docs/03_FastAPI_기초.md)
**학습 목표**: FastAPI 핵심 개념
- HTTP, WSGI/ASGI, 비동기
- Pydantic, SQLAlchemy
- API 설계 원칙

**소요 시간**: 5-7일  
**실습**: CRUD API 완성

---

### Phase 2: 설계 & 아키텍처 (Week 3-4)

#### 📘 [04_소프트웨어_설계.md](./docs/04_소프트웨어_설계.md)
**학습 목표**: 확장 가능한 구조 설계
- ERD 다이어그램
- 3계층 아키텍처
- 디자인 패턴 (Repository, Factory, Singleton)

**소요 시간**: 7일  
**실습**: 블로그 시스템 ERD 설계

---

#### 📘 [05_클린_아키텍처.md](./docs/05_클린_아키텍처.md)
**학습 목표**: 유지보수 쉬운 코드 작성
- MVC, SOLID 원칙
- 의존성 주입
- Service Layer 패턴

**소요 시간**: 5일  
**실습**: 기존 코드 리팩토링

---

### Phase 3: 테스트 & 품질 (Week 5-6)

#### 📘 [06_테스트_완벽_가이드.md](./docs/06_테스트_완벽_가이드.md)
**학습 목표**: 버그 없는 코드 작성
- Unit, Integration, E2E 테스트
- pytest 마스터
- 커버리지 80% 이상

**소요 시간**: 7일  
**실습**: 전체 프로젝트 테스트 작성

---

#### 📘 [07_CI_CD_파이프라인.md](./docs/07_CI_CD_파이프라인.md)
**학습 목표**: 자동화 배포
- GitHub Actions
- Docker 컨테이너화
- 자동 테스트 & 배포

**소요 시간**: 5일  
**실습**: CI/CD 파이프라인 구축

---

### Phase 4: 협업 & 오픈소스 (Week 7-8)

#### 📘 [08_Git_협업_마스터.md](./docs/08_Git_협업_마스터.md)
**학습 목표**: 팀 협업 능력
- Git Flow, PR, Code Review
- 커밋 메시지 규칙
- 오픈소스 기여

**소요 시간**: 5일  
**실습**: 오픈소스 프로젝트 기여 1건

---

#### 📘 [09_라이선스_이해.md](./docs/09_라이선스_이해.md)
**학습 목표**: 법적 이슈 방지
- MIT, Apache, GPL 비교
- 상업적 사용 가능 여부
- 프로젝트에 라이선스 추가

**소요 시간**: 2일

---

### Phase 5: 실전 프로젝트 (Week 9-12)

#### 📘 [10_최종_프로젝트.md](./docs/10_최종_프로젝트.md)
**학습 목표**: 실전 프로젝트 완성
- 요구사항부터 배포까지
- 협업 시뮬레이션
- 포트폴리오 제작

**프로젝트 아이디어**:
1. ML 모델 서빙 API (PyTorch 준비)
2. 데이터 파이프라인 시스템
3. 실시간 채팅 (WebSocket)

**소요 시간**: 4주

---

## 🎯 주차별 체크리스트

### Week 1
- [ ] Linux 명령어 50개 마스터
- [ ] DB 환경 구축 (Azure MySQL)
- [ ] FastAPI 기본 CRUD 완성

### Week 2
- [ ] ERD 설계 완료
- [ ] 3계층 아키텍처 구현
- [ ] Repository 패턴 적용

### Week 3
- [ ] Unit Test 작성 (커버리지 50%)
- [ ] Integration Test 추가
- [ ] 커버리지 80% 달성

### Week 4
- [ ] CI/CD 파이프라인 구축
- [ ] Docker 컨테이너화
- [ ] 자동 배포 설정

### Week 5-6
- [ ] Git Flow 적용
- [ ] 오픈소스 기여 1건
- [ ] Code Review 5건

### Week 7-8
- [ ] 최종 프로젝트 설계
- [ ] MVP 개발
- [ ] 테스트 & 문서화

### Week 9-12
- [ ] 프로젝트 완성
- [ ] 배포
- [ ] 포트폴리오 작성

---

## 📦 필수 도구 & 라이브러리

### 개발 환경
```bash
# 필수 설치
poetry add fastapi uvicorn sqlalchemy pydantic pymysql

# 테스트
poetry add pytest pytest-cov pytest-asyncio --group dev

# 코드 품질
poetry add black ruff pre-commit --group dev

# 배포
poetry add sentry-sdk python-dotenv
```

### 클라우드 & DB
- Azure Database for MySQL (현재 사용 중)
- AWS RDS (경험 있음)
- Docker for Desktop

---

## 🎓 학습 방법

### 하루 루틴 (2-3시간)
1. **이론 (30분)**: 문서 읽기
2. **실습 (1-1.5시간)**: 코드 작성
3. **복습 (30분)**: 주석 읽으며 이해
4. **도전 (30분)**: 오늘의 과제

### 주말 루틴
- 한 주 복습
- 미니 프로젝트
- 오픈소스 탐색

---

## ✅ 마스터 기준

숙련도를 체크하세요:

### FastAPI 마스터 체크리스트
- [ ] CRUD API를 30분 안에 구현
- [ ] 3계층 아키텍처를 자연스럽게 적용
- [ ] 에러 발생 시 로그 보고 즉시 해결
- [ ] 성능 병목 지점 파악 & 최적화
- [ ] API 문서 자동 생성 활용
- [ ] 테스트 커버리지 80% 이상
- [ ] CI/CD로 자동 배포

### 협업 마스터 체크리스트
- [ ] Git Flow 자연스럽게 사용
- [ ] 명확한 PR 작성
- [ ] 건설적인 Code Review
- [ ] 이슈 트래킹 능숙
- [ ] 문서화 습관

---

## 🚀 다음 단계: PyTorch & AI

FastAPI 마스터 후:

### Phase 6: AI/ML 백엔드 (Week 13+)
1. **PyTorch 기초**
2. **모델 서빙** (TorchServe, ONNX)
3. **MLOps** (MLflow, Kubeflow)
4. **GPU 활용** (CUDA)

---

## 📚 추가 학습 자료

### 공식 문서
- [FastAPI](https://fastapi.tiangolo.com/ko/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pytest](https://docs.pytest.org/)

### 책
- "Designing Data-Intensive Applications"
- "Clean Architecture" by Robert C. Martin

### 유튜브
- 코딩애플, 노마드 코더

---

**시작하기**: [01_왜_Linux인가.md](./docs/01_왜_Linux인가.md)부터 순서대로 읽으세요! 🎯
