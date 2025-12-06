from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.models import models
from app.database.database import engine
from app.routers import prompt

# 1. 데이터베이스 테이블 생성 (앱 시작 시 자동 실행)
models.Base.metadata.create_all(bind=engine)

# 2. FastAPI 앱 초기화
app = FastAPI(
    title="Refine AI",
    description="AI Prompt Refinement Service",
    version="1.0.0"
)

# 3. 라우터 등록
app.include_router(prompt.router)

# 4. 정적 파일 (UI) 서빙
@app.get("/")
def read_root():
    # UI 파일 서빙
    return FileResponse("templates/index.html")

@app.get("/my-info")
def read_my_info():
    # 내 정보/통계 페이지 서빙
    return FileResponse("templates/my_info.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
