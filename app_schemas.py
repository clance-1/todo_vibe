from pydantic import BaseModel, Field
from typing import Optional

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1)
    category: str
    date: str

class TodoUpdate(BaseModel):
    title: Optional[str]
    category: Optional[str]
    date: Optional[str]
    completed: Optional[bool]

class TodoResponse(BaseModel):
    id: int
    title: str
    category: str
    date: str
    completed: bool


class ErrorResponse(BaseModel):
    error: str
    details: Optional[list] = None
