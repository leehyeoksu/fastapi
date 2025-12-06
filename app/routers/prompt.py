from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models import models
from app.schemas import schemas
from app.services import service
from app.database.database import get_db

router = APIRouter(
    prefix="/api",
    tags=["prompts"]
)

@router.post("/refine", response_model=schemas.RefineResponse)
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

@router.get("/history", response_model=List[schemas.HistoryResponse])
def get_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    저장된 프롬프트 변환 기록을 조회합니다.
    """
    history = db.query(models.PromptHistory).order_by(models.PromptHistory.id.desc()).offset(skip).limit(limit).all()
    return history

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    카테고리별 사용 빈도 통계를 반환합니다.
    """
    from sqlalchemy import func
    # 카테고리별 개수 집계 (GROUP BY category)
    stats = db.query(models.PromptHistory.category, func.count(models.PromptHistory.category)).group_by(models.PromptHistory.category).all()
    
    # 리스트 딕셔너리로 변환 [{"category": "Coding", "count": 5}, ...]
    return [{"category": category, "count": count} for category, count in stats]

@router.delete("/history/{history_id}")
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

@router.delete("/history")
def clear_all_history(db: Session = Depends(get_db)):
    """
    모든 히스토리를 삭제합니다.
    """
    db.query(models.PromptHistory).delete()
    db.commit()
    return {"message": "All history cleared"}
