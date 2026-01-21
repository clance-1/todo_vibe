"""API 입력/출력용 Pydantic 스키마 정의.

이 파일은 API 요청/응답 유효성 검사용 Pydantic 모델을 포함합니다.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date


class TodoCreate(BaseModel):
    """할일 생성용 입력 스키마.

    필드 유효성(예: `title` 최소 길이, `category` 제한 등)을 정의합니다.
    """
    title: str = Field(..., min_length=1)
    category: Literal['study', 'personal', 'work']
    date: date


class TodoUpdate(BaseModel):
    """할일 업데이트용 입력 스키마. 모든 필드는 선택적입니다."""
    title: Optional[str] = None
    category: Optional[Literal['study', 'personal', 'work']] = None
    date: Optional[date] = None
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    """API 응답으로 반환되는 할일 모델 스키마."""
    id: int
    title: str
    category: str
    date: str
    completed: bool


class ErrorResponse(BaseModel):
    """에러 응답 스키마.

    `details`는 검증 오류 등 추가 정보를 담는 선택적 필드입니다.
    """
    error: str
    details: Optional[list] = None
