from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from app.models.item import Item
from app.models.schemas import ItemCreate, ItemUpdate

# アイテムの取得（全件）
async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Item]:
    query = select(Item).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# IDによるアイテムの取得
async def get_item(db: AsyncSession, item_id: int) -> Optional[Item]:
    query = select(Item).where(Item.id == item_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# バーコードによるアイテムの取得
async def get_item_by_barcode(db: AsyncSession, barcode: str) -> Optional[Item]:
    query = select(Item).where(Item.barcode == barcode)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# アイテムの作成
async def create_item(db: AsyncSession, item: ItemCreate) -> Item:
    db_item = Item(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

# アイテムの更新
async def update_item(db: AsyncSession, item_id: int, item: ItemUpdate) -> Optional[Item]:
    update_data = item.dict(exclude_unset=True)
    if not update_data:
        return None
    
    query = update(Item).where(Item.id == item_id).values(**update_data)
    await db.execute(query)
    await db.commit()
    
    return await get_item(db, item_id)

# アイテムの削除
async def delete_item(db: AsyncSession, item_id: int) -> bool:
    query = delete(Item).where(Item.id == item_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0 