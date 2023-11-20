from pydantic import BaseModel, Field
from typing import Optional


class Todo(BaseModel):
    id: Optional[int] = None
    description: str = Field(min_length=5, max_length=500)
    complete: bool = Field(default=False)
