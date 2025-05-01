from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas import Location
from app.service import location as location_crud

router = APIRouter()

@router.get("/locations", response_model=List[Location])
async def read_locations(db: AsyncSession = Depends(get_db)):
    """
    すべてのロケーションを取得します。
    """
    locations = await location_crud.get_locations(db)
    return locations