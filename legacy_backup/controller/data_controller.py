from fastapi import APIRouter, HTTPException, status
from typing import Dict, List
from datetime import datetime
from controller.schemas import DataInput, DataResponse

# APIRouter 생성 (prefix 제거)
router = APIRouter(
    tags=["data"],
    responses={404: {"description": "Not found"}},
)

# 메모리에 데이터를 저장할 딕셔너리
data_store: Dict[int, DataResponse] = {}
next_id = 1


@router.post("/data", response_model=DataResponse, status_code=status.HTTP_201_CREATED)
async def create_data(data: DataInput):
    """
    데이터 저장 엔드포인트
    
    프론트엔드에서 JSON 데이터를 받아 메모리에 저장합니다.
    
    - **name**: 데이터 이름 (필수)
    - **value**: 데이터 값 (필수)
    - **description**: 데이터 설명 (선택)
    
    Returns:
        저장된 데이터 (ID와 생성 시간 포함)
    """
    global next_id
    
    # 새로운 데이터 객체 생성
    new_data = DataResponse(
        id=next_id,
        name=data.name,
        value=data.value,
        description=data.description,
        created_at=datetime.now().isoformat()
    )
    
    # 메모리에 저장
    data_store[next_id] = new_data
    next_id += 1
    
    return new_data


@router.get("/data", response_model=List[DataResponse])
async def get_all_data():
    """
    모든 데이터 조회 엔드포인트
    
    저장된 모든 데이터를 반환합니다.
    
    Returns:
        저장된 모든 데이터 리스트
    """
    if not data_store:
        return []
    
    return list(data_store.values())


@router.get("/data/{data_id}", response_model=DataResponse)
async def get_data_by_id(data_id: int):
    """
    특정 ID의 데이터 조회 엔드포인트
    
    지정된 ID의 데이터를 반환합니다.
    
    - **data_id**: 조회할 데이터의 ID
    
    Returns:
        해당 ID의 데이터
        
    Raises:
        HTTPException: 데이터가 없을 경우 404 에러
    """
    if data_id not in data_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {data_id}에 해당하는 데이터를 찾을 수 없습니다."
        )
    
    return data_store[data_id]


@router.delete("/data/{data_id}")
async def delete_data(data_id: int):
    """
    데이터 삭제 엔드포인트
    
    지정된 ID의 데이터를 삭제합니다.
    
    - **data_id**: 삭제할 데이터의 ID
    
    Returns:
        삭제 성공 메시지
        
    Raises:
        HTTPException: 데이터가 없을 경우 404 에러
    """
    if data_id not in data_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {data_id}에 해당하는 데이터를 찾을 수 없습니다."
        )
    
    deleted_data = data_store.pop(data_id)
    return {
        "message": f"ID {data_id}의 데이터가 삭제되었습니다.",
        "deleted_data": deleted_data
    }
