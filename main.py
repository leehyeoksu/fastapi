from app.main import app

if __name__ == "__main__":
    import uvicorn
    # uvicorn 실행 시 reload 옵션과 함께 html 파일 변경도 감지하도록 설정
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, reload_includes=["*.html"])
