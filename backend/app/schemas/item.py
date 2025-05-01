from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    id: Optional[int] = None
    barcode: Optional[int] = None
    name: Optional[str] = None
    category_id: Optional[int] = None
    min_threshold: int = 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True