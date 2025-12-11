from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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

# 3. 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [개발용] 브라우저 캐시 강제 비활성화 미들웨어
@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# 4. 라우터 등록 (Original 3. is now 4.)
app.include_router(prompt.router)

# 4.5 정적 파일 마운트 (Original 3.5 is now 4.5)
app.mount("/static", StaticFiles(directory="static"), name="static")
# 템플릿 설정 (절대 경로로 변경하여 감지 정확도 향상)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(BASE_DIR, "..", "templates")
templates = Jinja2Templates(directory=templates_dir)
templates.env.auto_reload = True


# 4. 정적 파일 (UI) 서빙
@app.get("/")
def read_root(request: Request):
    # UI 파일 서빙
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/my-info")
def read_my_info(request: Request):
    # 내 정보/통계 페이지 서빙
    return templates.TemplateResponse("my_info.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, reload_includes=["*.html"])
