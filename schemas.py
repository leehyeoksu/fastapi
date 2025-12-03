from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 요청 데이터 모델
class PromptRequest(BaseModel):
    prompt: str
    style: str
    category: Optional[str] = "Auto" # 사용자가 직접 선택한 카테고리 (기본값: 자동)
    model: Optional[str] = "gpt-3.5-turbo" # 사용할 OpenAI 모델 (기본값: gpt-3.5-turbo)

# 분석 결과 모델
class AnalysisResult(BaseModel):
    category: str # 카테고리 추가
    missing_context: bool
    missing_format: bool
    suggestions: List[str]

# 최종 응답 모델
class RefineResponse(BaseModel):
    original_prompt: str
    refined_prompt: str
    analysis: AnalysisResult
    tips: List[str]

# 히스토리 응답 모델 (DB 저장된 것 조회용)
class HistoryResponse(BaseModel):
    id: int
    original_prompt: str
    refined_prompt: str
    category: Optional[str] = "General" # 조회 시 카테고리 반환
    created_at: datetime

    class Config:
        from_attributes = True
