from pydantic import BaseModel
from datetime import datetime

class Stock(BaseModel):
    id: int
    item_id: int
    location_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True