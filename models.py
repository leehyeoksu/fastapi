from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class PromptHistory(Base):
    __tablename__ = "prompt_history"

    id = Column(Integer, primary_key=True, index=True)
    original_prompt = Column(Text, nullable=False)
    refined_prompt = Column(Text, nullable=True)
    
    # 분석 결과 저장
    category = Column(String, default="General") # 질문 종류 (Coding, Image, Writing 등)
    missing_context = Column(Boolean, default=False)
    missing_format = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
