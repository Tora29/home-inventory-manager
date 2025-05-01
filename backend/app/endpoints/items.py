from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.service import item as item_crud
from app.schemas import Item

router = APIRouter()

@router.get("/items/", response_model=List[Item])
async def read_items(
    skip: int = 0, 
    limit: int = 25, 
    db: AsyncSession = Depends(get_db)
):
    """
    すべてのアイテムを取得します。
    """
    items = await item_crud.get_items(db, skip=skip, limit=limit)
    return items