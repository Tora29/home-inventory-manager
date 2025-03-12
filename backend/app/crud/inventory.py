from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from app.models.inventory import Inventory
from app.models.schemas import InventoryCreate, InventoryUpdate

# 在庫の取得（全件）
async def get_inventories(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Inventory]:
    query = select(Inventory).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# IDによる在庫の取得
async def get_inventory(db: AsyncSession, inventory_id: int) -> Optional[Inventory]:
    query = select(Inventory).where(Inventory.id == inventory_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# アイテムIDによる在庫の取得
async def get_inventory_by_item_id(db: AsyncSession, item_id: int) -> Optional[Inventory]:
    query = select(Inventory).where(Inventory.item_id == item_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 在庫の作成
async def create_inventory(db: AsyncSession, inventory: InventoryCreate) -> Inventory:
    # 同じitem_idのレコードがあるか確認
    existing = await get_inventory_by_item_id(db, inventory.item_id)
    if existing:
        # 既存の在庫を更新
        query = update(Inventory).where(Inventory.item_id == inventory.item_id).values(quantity=inventory.quantity)
        await db.execute(query)
        await db.commit()
        await db.refresh(existing)
        return existing
    
    # 新規作成
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    await db.commit()
    await db.refresh(db_inventory)
    return db_inventory

# 在庫の更新
async def update_inventory(db: AsyncSession, inventory_id: int, inventory: InventoryUpdate) -> Optional[Inventory]:
    update_data = inventory.dict(exclude_unset=True)
    if not update_data:
        return None
    
    query = update(Inventory).where(Inventory.id == inventory_id).values(**update_data)
    await db.execute(query)
    await db.commit()
    
    return await get_inventory(db, inventory_id)

# アイテムIDによる在庫の更新
async def update_inventory_by_item_id(db: AsyncSession, item_id: int, quantity: int) -> Optional[Inventory]:
    # 既存の在庫を確認
    existing = await get_inventory_by_item_id(db, item_id)
    if not existing:
        # レコードがなければ作成
        return await create_inventory(db, InventoryCreate(item_id=item_id, quantity=quantity))
    
    # 在庫を更新
    query = update(Inventory).where(Inventory.item_id == item_id).values(quantity=quantity)
    await db.execute(query)
    await db.commit()
    
    return await get_inventory_by_item_id(db, item_id)

# 在庫の削除
async def delete_inventory(db: AsyncSession, inventory_id: int) -> bool:
    query = delete(Inventory).where(Inventory.id == inventory_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0 