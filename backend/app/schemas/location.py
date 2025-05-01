from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Location(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True