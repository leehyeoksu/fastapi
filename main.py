from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

import models, schemas, service
from database import SessionLocal, engine, get_db

# 1. 데이터베이스 테이블 생성 (앱 시작 시 자동 실행)
models.Base.metadata.create_all(bind=engine)

# 2. FastAPI 앱 초기화
app = FastAPI(
    title="Refine AI",
    description="AI Prompt Refinement Service",
    version="1.0.0"
)

# 3. API 엔드포인트 정의

@app.get("/")
def read_root():
    # UI 파일 서빙
    return FileResponse("templates/index.html")

@app.get("/my-info")
def read_my_info():
    # 내 정보/통계 페이지 서빙
    return FileResponse("templates/my_info.html")

@app.post("/api/refine", response_model=schemas.RefineResponse)
def refine_prompt(request: schemas.PromptRequest, db: Session = Depends(get_db)):
    """
    프롬프트를 분석하고 개선합니다. 결과는 DB에 저장됩니다.
    """
    # 1. AI 서비스 호출
    result = service.process_prompt_with_ai(request.prompt, request.style, request.category)
    
    # 2. DB에 히스토리 저장
    db_history = models.PromptHistory(
        original_prompt=result.original_prompt,
        refined_prompt=result.refined_prompt,
        category=result.analysis.category, # 카테고리 저장
        missing_context=result.analysis.missing_context,
        missing_format=result.analysis.missing_format
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    
    return result

@app.get("/api/history", response_model=List[schemas.HistoryResponse])
def get_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    저장된 프롬프트 변환 기록을 조회합니다.
    """
    history = db.query(models.PromptHistory).order_by(models.PromptHistory.id.desc()).offset(skip).limit(limit).all()
    return history

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    카테고리별 사용 빈도 통계를 반환합니다.
    """
    from sqlalchemy import func
    # 카테고리별 개수 집계 (GROUP BY category)
    stats = db.query(models.PromptHistory.category, func.count(models.PromptHistory.category)).group_by(models.PromptHistory.category).all()
    
    # 리스트 딕셔너리로 변환 [{"category": "Coding", "count": 5}, ...]
    return [{"category": category, "count": count} for category, count in stats]

@app.delete("/api/history/{history_id}")
def delete_history_item(history_id: int, db: Session = Depends(get_db)):
    """
    특정 히스토리 항목을 삭제합니다.
    """
    item = db.query(models.PromptHistory).filter(models.PromptHistory.id == history_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

@app.delete("/api/history")
def clear_all_history(db: Session = Depends(get_db)):
    """
    모든 히스토리를 삭제합니다.
    """
    db.query(models.PromptHistory).delete()
    db.commit()
    return {"message": "All history cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
