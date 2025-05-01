from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Category(CategoryBase):
    pass