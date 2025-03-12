from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.crud import inventory as inventory_crud
from app.models.schemas import Inventory, InventoryCreate, InventoryUpdate, InventoryDetail

router = APIRouter()

@router.get("/inventory/", response_model=List[Inventory])
async def read_inventories(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """
    すべての在庫情報を取得します。
    """
    inventories = await inventory_crud.get_inventories(db, skip=skip, limit=limit)
    return inventories

@router.get("/inventory/{inventory_id}", response_model=Inventory)
async def read_inventory(
    inventory_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDの在庫情報を取得します。
    """
    db_inventory = await inventory_crud.get_inventory(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return db_inventory

@router.get("/inventory/item/{item_id}", response_model=Inventory)
async def read_inventory_by_item_id(
    item_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたアイテムIDの在庫情報を取得します。
    """
    db_inventory = await inventory_crud.get_inventory_by_item_id(db, item_id=item_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return db_inventory

@router.post("/inventory/", response_model=Inventory, status_code=status.HTTP_201_CREATED)
async def create_inventory(
    inventory: InventoryCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    新しい在庫情報を作成します。
    """
    return await inventory_crud.create_inventory(db=db, inventory=inventory)

@router.put("/inventory/{inventory_id}", response_model=Inventory)
async def update_inventory(
    inventory_id: int, 
    inventory: InventoryUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDの在庫情報を更新します。
    """
    db_inventory = await inventory_crud.get_inventory(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    updated_inventory = await inventory_crud.update_inventory(db=db, inventory_id=inventory_id, inventory=inventory)
    return updated_inventory

@router.put("/inventory/item/{item_id}", response_model=Inventory)
async def update_inventory_by_item_id(
    item_id: int, 
    quantity: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたアイテムIDの在庫数量を更新します。
    """
    updated_inventory = await inventory_crud.update_inventory_by_item_id(db=db, item_id=item_id, quantity=quantity)
    return updated_inventory

@router.delete("/inventory/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(
    inventory_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDの在庫情報を削除します。
    """
    db_inventory = await inventory_crud.get_inventory(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    success = await inventory_crud.delete_inventory(db=db, inventory_id=inventory_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete inventory")
    
    return None 