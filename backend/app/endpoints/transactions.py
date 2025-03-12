from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.crud import transaction as transaction_crud
from app.models.schemas import Transaction, TransactionCreate, TransactionUpdate, TransactionDetail

router = APIRouter()

@router.get("/transactions/", response_model=List[Transaction])
async def read_transactions(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """
    すべてのトランザクション（入出庫履歴）を取得します。
    """
    transactions = await transaction_crud.get_transactions(db, skip=skip, limit=limit)
    return transactions

@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def read_transaction(
    transaction_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDのトランザクションを取得します。
    """
    db_transaction = await transaction_crud.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.get("/transactions/item/{item_id}", response_model=List[Transaction])
async def read_transactions_by_item_id(
    item_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたアイテムIDのトランザクション履歴を取得します。
    """
    transactions = await transaction_crud.get_transactions_by_item_id(db, item_id=item_id, skip=skip, limit=limit)
    return transactions

@router.post("/transactions/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    新しいトランザクション（入出庫記録）を作成します。
    在庫数量も自動的に更新されます。
    """
    return await transaction_crud.create_transaction(db=db, transaction=transaction)

@router.put("/transactions/{transaction_id}", response_model=Transaction)
async def update_transaction(
    transaction_id: int, 
    transaction: TransactionUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDのトランザクションを更新します。
    必要に応じて在庫数量も調整されます。
    """
    db_transaction = await transaction_crud.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    updated_transaction = await transaction_crud.update_transaction(db=db, transaction_id=transaction_id, transaction=transaction)
    return updated_transaction

@router.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDのトランザクションを削除します。
    在庫数量も調整されます。
    """
    db_transaction = await transaction_crud.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    success = await transaction_crud.delete_transaction(db=db, transaction_id=transaction_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete transaction")
    
    return None 