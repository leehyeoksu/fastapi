from pydantic import BaseModel, Field
from typing import Optional


class DataInput(BaseModel):
    """프론트엔드에서 받을 데이터 모델"""
    name: str = Field(..., description="데이터 이름", min_length=1)
    value: str = Field(..., description="데이터 값", min_length=1)
    description: Optional[str] = Field(None, description="데이터 설명 (선택사항)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "테스트",
                "value": "데이터1",
                "description": "샘플 데이터입니다"
            }
        }


class DataResponse(BaseModel):
    """저장된 데이터를 반환할 때 사용하는 모델 (ID 포함)"""
    id: int
    name: str
    value: str
    description: Optional[str]
    created_at: str
