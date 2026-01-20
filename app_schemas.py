from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1)
    category: Literal['study', 'personal', 'work']
    date: date


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[Literal['study', 'personal', 'work']] = None
    date: Optional[date] = None
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    category: str
    date: str
    completed: bool


class ErrorResponse(BaseModel):
    error: str
    details: Optional[list] = None
