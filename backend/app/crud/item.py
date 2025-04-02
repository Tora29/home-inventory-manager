from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.item import Item

# アイテムの取得（全件）
async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Item]:
    query = select(Item).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# バーコードでアイテムを取得
async def get_item_by_barcode(db: AsyncSession, barcode: str) -> Optional[Item]:
    query = select(Item).where(Item.barcode == barcode)
    result = await db.execute(query)
    return result.scalars().first()
