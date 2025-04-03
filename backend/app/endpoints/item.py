from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.crud import item as item_crud
from app.models.schemas import Item, ItemCreate
from app.models.item import Item as ItemModel

router = APIRouter()

@router.get("/items/", response_model=List[Item])
async def read_items(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """
    すべてのアイテムを取得します。
    """
    items = await item_crud.get_items(db, skip=skip, limit=limit)
    return items

@router.post("/items/", response_model=Item)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    新しいアイテムを作成します。
    """
    # 同じバーコードの商品がすでに存在する場合は確認
    if item.barcode:
        existing_item = await item_crud.get_item_by_barcode(db, item.barcode)
        if existing_item:
            return existing_item
    
    # 新しい商品を作成
    db_item = ItemModel(
        name=item.name,
        barcode=item.barcode,
        category_id=item.category_id,
        note=item.note,
        min_threshold=item.min_threshold or 1
    )
    
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    
    return db_item