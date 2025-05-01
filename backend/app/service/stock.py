from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.stock import Stock

# 在庫の取得（全件）
async def get_stocks(db: AsyncSession, skip: int = 0, limit: int = 25) -> List[Stock]:
    """すべての在庫を取得する"""
    query = select(Stock).offset(skip).limit(limit)
    result = await db.execute(query)
    stocks = result.scalars().all()
    return stocks
