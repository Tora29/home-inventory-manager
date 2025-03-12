from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.crud import item as item_crud, inventory as inventory_crud
from app.models.schemas import Item, ItemCreate, ItemUpdate, ItemDetail

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

@router.get("/items/{item_id}", response_model=Item)
async def read_item(
    item_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDのアイテムを取得します。
    """
    db_item = await item_crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.get("/items/barcode/{barcode}", response_model=Item)
async def read_item_by_barcode(
    barcode: str, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたバーコードのアイテムを取得します。
    """
    db_item = await item_crud.get_item_by_barcode(db, barcode=barcode)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item with this barcode not found")
    return db_item

@router.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    新しいアイテムを作成します。
    """
    # 同じバーコードのアイテムが既に存在するか確認
    if item.barcode:
        existing_item = await item_crud.get_item_by_barcode(db, barcode=item.barcode)
        if existing_item:
            raise HTTPException(
                status_code=400, 
                detail=f"Item with barcode {item.barcode} already exists (ID: {existing_item.id})"
            )
    
    return await item_crud.create_item(db=db, item=item)

@router.put("/items/{item_id}", response_model=Item)
async def update_item(
    item_id: int, 
    item: ItemUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDのアイテムを更新します。
    """
    db_item = await item_crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # バーコードが更新されていて、かつ他のアイテムがそのバーコードを使用している場合はエラー
    if item.barcode and item.barcode != db_item.barcode:
        existing_item = await item_crud.get_item_by_barcode(db, barcode=item.barcode)
        if existing_item and existing_item.id != item_id:
            raise HTTPException(
                status_code=400, 
                detail=f"Item with barcode {item.barcode} already exists (ID: {existing_item.id})"
            )
    
    updated_item = await item_crud.update_item(db=db, item_id=item_id, item=item)
    return updated_item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDのアイテムを削除します。
    """
    db_item = await item_crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    success = await item_crud.delete_item(db=db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete item")
    
    return None

@router.get("/items/details/{item_id}", response_model=ItemDetail)
async def read_item_detail(
    item_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    アイテムの詳細情報（カテゴリ情報と現在の在庫数を含む）を取得します。
    """
    db_item = await item_crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # 在庫情報を取得
    inventory = await inventory_crud.get_inventory_by_item_id(db, item_id=item_id)
    
    # アイテム情報を詳細なスキーマに変換
    item_detail = ItemDetail.from_orm(db_item)
    
    # 在庫数量を設定
    item_detail.current_quantity = inventory.quantity if inventory else 0
    
    return item_detail 