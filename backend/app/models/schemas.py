from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

# ベースモデル
class BaseModelConfig(BaseModel):
    class Config:
        orm_mode = True

# カテゴリ関連のスキーマ
class CategoryBase(BaseModel):
    category_name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# アイテム関連のスキーマ
class ItemBase(BaseModel):
    item_name: str
    barcode: Optional[str] = None
    category_id: Optional[int] = None
    note: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    item_name: Optional[str] = None
    barcode: Optional[str] = None
    category_id: Optional[int] = None
    note: Optional[str] = None

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ItemDetail(Item):
    category: Optional[Category] = None
    current_quantity: Optional[int] = None

# 在庫関連のスキーマ
class InventoryBase(BaseModel):
    item_id: int
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None

class Inventory(InventoryBase):
    id: int
    updated_at: datetime
    
    class Config:
        orm_mode = True

class InventoryDetail(Inventory):
    item: Item

# トランザクション関連のスキーマ
class TransactionBase(BaseModel):
    item_id: int
    transaction_type: str  # "IN" または "OUT"
    quantity: int
    note: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    transaction_type: Optional[str] = None
    quantity: Optional[int] = None
    note: Optional[str] = None

class Transaction(TransactionBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class TransactionDetail(Transaction):
    item: Item 