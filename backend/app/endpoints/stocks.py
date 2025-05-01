from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.service import stock as stock_crud
from app.schemas import Stock

router = APIRouter()

@router.get("/stocks/", response_model=List[Stock])
async def read_stocks(
    skip: int = 0, 
    limit: int = 25, 
    db: AsyncSession = Depends(get_db)
):
    """
    すべての在庫情報を取得します。
    """
    stocks = await stock_crud.get_stocks(db, skip=skip, limit=limit)
    return stocks