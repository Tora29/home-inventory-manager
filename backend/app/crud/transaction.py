from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, desc

from app.models.transaction import Transaction
from app.models.schemas import TransactionCreate, TransactionUpdate
from app.crud import inventory as inventory_crud

# トランザクションの取得（全件）
async def get_transactions(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Transaction]:
    query = select(Transaction).order_by(desc(Transaction.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# IDによるトランザクションの取得
async def get_transaction(db: AsyncSession, transaction_id: int) -> Optional[Transaction]:
    query = select(Transaction).where(Transaction.id == transaction_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# アイテムIDによるトランザクション一覧の取得
async def get_transactions_by_item_id(db: AsyncSession, item_id: int, skip: int = 0, limit: int = 100) -> List[Transaction]:
    query = select(Transaction).where(Transaction.item_id == item_id).order_by(desc(Transaction.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# トランザクションの作成（在庫も自動更新）
async def create_transaction(db: AsyncSession, transaction: TransactionCreate) -> Transaction:
    # トランザクションを作成
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    
    # 在庫を更新
    item_id = transaction.item_id
    inventory = await inventory_crud.get_inventory_by_item_id(db, item_id)
    
    current_quantity = 0
    if inventory:
        current_quantity = inventory.quantity
    
    # 入荷か出荷かで数量を調整
    if transaction.transaction_type.upper() == "IN":
        new_quantity = current_quantity + transaction.quantity
    else:  # "OUT"
        new_quantity = current_quantity - transaction.quantity
        if new_quantity < 0:
            new_quantity = 0  # マイナスにはならないようにする
    
    # 在庫を更新
    await inventory_crud.update_inventory_by_item_id(db, item_id, new_quantity)
    
    return db_transaction

# トランザクションの更新
async def update_transaction(db: AsyncSession, transaction_id: int, transaction: TransactionUpdate) -> Optional[Transaction]:
    update_data = transaction.dict(exclude_unset=True)
    if not update_data:
        return None
    
    # トランザクションを取得
    original_transaction = await get_transaction(db, transaction_id)
    if not original_transaction:
        return None
    
    # 数量や取引タイプが変更された場合は、在庫も調整する必要がある
    need_inventory_update = False
    quantity_diff = 0
    
    if "quantity" in update_data or "transaction_type" in update_data:
        need_inventory_update = True
        
        # 新しい数量と取引タイプを決定
        new_quantity = update_data.get("quantity", original_transaction.quantity)
        new_type = update_data.get("transaction_type", original_transaction.transaction_type)
        
        # 元の取引を巻き戻す (逆の操作を行う)
        if original_transaction.transaction_type.upper() == "IN":
            quantity_diff -= original_transaction.quantity
        else:  # "OUT"
            quantity_diff += original_transaction.quantity
        
        # 新しい取引を適用
        if new_type.upper() == "IN":
            quantity_diff += new_quantity
        else:  # "OUT"
            quantity_diff -= new_quantity
    
    # トランザクションを更新
    query = update(Transaction).where(Transaction.id == transaction_id).values(**update_data)
    await db.execute(query)
    await db.commit()
    
    # 在庫の調整が必要な場合
    if need_inventory_update:
        item_id = original_transaction.item_id
        inventory = await inventory_crud.get_inventory_by_item_id(db, item_id)
        
        if inventory:
            new_inventory_quantity = max(0, inventory.quantity + quantity_diff)  # マイナスにならないように
            await inventory_crud.update_inventory_by_item_id(db, item_id, new_inventory_quantity)
    
    return await get_transaction(db, transaction_id)

# トランザクションの削除（在庫も自動調整）
async def delete_transaction(db: AsyncSession, transaction_id: int) -> bool:
    # トランザクションを取得
    transaction = await get_transaction(db, transaction_id)
    if not transaction:
        return False
    
    # 削除前に在庫調整用の情報を記録
    item_id = transaction.item_id
    transaction_type = transaction.transaction_type
    quantity = transaction.quantity
    
    # トランザクションを削除
    query = delete(Transaction).where(Transaction.id == transaction_id)
    result = await db.execute(query)
    await db.commit()
    
    if result.rowcount > 0:
        # 在庫を調整（トランザクションの逆操作）
        inventory = await inventory_crud.get_inventory_by_item_id(db, item_id)
        if inventory:
            current_quantity = inventory.quantity
            
            # 入荷の取消は在庫減、出荷の取消は在庫増
            if transaction_type.upper() == "IN":
                new_quantity = max(0, current_quantity - quantity)  # マイナスにならないように
            else:  # "OUT"
                new_quantity = current_quantity + quantity
                
            await inventory_crud.update_inventory_by_item_id(db, item_id, new_quantity)
        
        return True
    
    return False 