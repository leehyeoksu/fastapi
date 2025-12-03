# 📘 07_CI_CD_파이프라인

**학습 목표**: 자동화된 테스트 & 배포 시스템 구축

---

## 🔄 CI/CD란?

### CI (Continuous Integration) - 지속적 통합
**뜻**: 코드 변경 시 자동으로 테스트

**흐름**:
```
코드 푸시 → 자동 테스트 → 통과하면 Merge
```

### CD (Continuous Deployment) - 지속적 배포
**뜻**: 테스트 통과 시 자동으로 배포

**흐름**:
```
테스트 통과 → 자동 빌드 → 프로덕션 배포
```

**왜 필요?**:
- 수동 테스트 → 빠뜨릴 수 있음
- 수동 배포 → 실수할 수 있음
- 자동화 → 안정적이고 빠름

🔗 [CI/CD 개념](https://www.redhat.com/ko/topics/devops/what-is-ci-cd)

---

## 🚀 GitHub Actions 완벽 가이드

### .github/workflows/test.yml

```yaml
name: Test & Lint

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      # 테스트용 DB
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: password
          MYSQL_DATABASE: test_db
        ports:
          - 3306:3306
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH
    
    - name: Install dependencies
      run: poetry install
    
    - name: Run tests
      env:
        DATABASE_URL: mysql://root:password@localhost:3306/test_db
      run: |
        poetry run pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
    
    - name: Lint with Ruff
      run: poetry run ruff check .
    
    - name: Format check with Black
      run: poetry run black --check .
```

### .github/workflows/deploy.yml

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:  # 수동 실행 가능

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t myapp:${{ github.sha }} .
        docker tag myapp:${{ github.sha }} myapp:latest
    
    - name: Login to Azure Container Registry
      uses: azure/docker-login@v1
      with:
        login-server: myregistry.azurecr.io
        username: ${{ secrets.AZURE_USERNAME }}
        password: ${{ secrets.AZURE_PASSWORD }}
    
    - name: Push to ACR
      run: |
        docker push myregistry.azurecr.io/myapp:latest
    
    - name: Deploy to Azure App Service
      uses: azure/webapps-deploy@v2
      with:
        app-name: my-fastapi-app
        images: myregistry.azurecr.io/myapp:latest
```

🔗 [GitHub Actions 공식 문서](https://docs.github.com/actions)

---

## 🐳 Docker 완벽 가이드

### Dockerfile

```dockerfile
# [Stage 1] 빌드 스테이지
FROM python:3.12-slim as builder

WORKDIR /app

# Poetry 설치
RUN pip install poetry

# 의존성만 먼저 복사 (캐싱 활용)
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# [Stage 2] 실행 스테이지 (경량화)
FROM python:3.12-slim

WORKDIR /app

# 빌드 스테이지에서 requirements.txt 복사
COPY --from=builder /app/requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . .

# 포트 노출
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql://user:pass@db:3306/mydb
    depends_on:
      - db
    volumes:
      - .:/app
    restart: unless-stopped
  
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: mydb
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  mysql_data:
```

**사용법**:
```bash
# 빌드 & 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 종료
docker-compose down
```

🔗 [Docker 튜토리얼](https://docs.docker.com/get-started/)

---

## 🔧 .dockerignore

```
# 불필요한 파일 제외 (이미지 크기 감소)
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build

.git
.gitignore
.env
.venv
venv/

# 테스트
.pytest_cache
.coverage
htmlcov/

# IDE
.vscode/
.idea/

# 문서
*.md
docs/
```

---

## 📦 배포 전략

### Blue-Green Deployment
```
Blue (현재)   Green (새 버전)
    ↓              ↓
   유저 ----→ 트래픽 전환
```

### Rolling Update
```
서버1 업데이트 → 서버2 업데이트 → 서버3 업데이트
(순차적으로 진행, 무중단)
```

### Canary Deployment
```
90% 트래픽 → 기존 버전
10% 트래픽 → 새 버전 (테스트)
```

---

## 🎯 실습 과제

### Day 1: GitHub Actions 설정
```bash
# 1. .github/workflows/test.yml 생성
# 2. GitHub에 푸시
git add .
git commit -m "Add CI workflow"
git push

# 3. GitHub Actions 탭에서 확인
# https://github.com/username/repo/actions
```

### Day 2: Docker 이미지 생성
```bash
# 1. Dockerfile 작성
# 2. 빌드
docker build -t myapp .

# 3. 실행
docker run -p 8000:8000 myapp

# 4. 테스트
curl http://localhost:8000/docs
```

### Day 3: Azure 배포
```bash
# 1. Azure Container Registry 생성
az acr create --name myregistry --resource-group mygroup --sku Basic

# 2. 로그인
az acr login --name myregistry

# 3. 이미지 푸시
docker tag myapp myregistry.azurecr.io/myapp:latest
docker push myregistry.azurecr.io/myapp:latest

# 4. App Service 배포
az webapp create \
  --name myapp \
  --plan myplan \
  --deployment-container-image-name myregistry.azurecr.io/myapp:latest
```

---

## 💪 레벨업 과제

### 🌟 초급
- [ ] GitHub Actions로 테스트 자동화
- [ ] Docker 이미지 빌드
- [ ] docker-compose로 로컬 실행

### 🌟🌟 중급
- [ ] 자동 배포 파이프라인
- [ ] 환경별 설정 (dev, staging, prod)
- [ ] Secrets 관리

### 🌟🌟🌟 고급
- [ ] Blue-Green Deployment
- [ ] 모니터링 (Prometheus, Grafana)
- [ ] 로그 수집 (ELK Stack)

---

## 📚 추가 자료

- [GitHub Actions 마켓플레이스](https://github.com/marketplace?type=actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Azure DevOps](https://learn.microsoft.com/azure/devops/)

---

**다음 학습**: [08_Git_협업_마스터.md](./08_Git_협업_마스터.md) 🚀
