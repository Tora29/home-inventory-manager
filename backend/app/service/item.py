from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.item import Item

# アイテムの取得（全件）
async def get_items(db: AsyncSession, skip: int = 0, limit: int = 25) -> List[Item]:
    """すべてのアイテムを取得する"""
    query = select(Item).offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    return items
