from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

# ベースモデル
class BaseModelConfig(BaseModel):
    class Config:
        from_attributes = True
        orm_mode = True

# カテゴリ関連のスキーマ
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class Category(CategoryBase):
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True

# アイテム関連のスキーマ
class ItemBase(BaseModel):
    name: str
    barcode: Optional[str] = None
    category_id: Optional[int] = None
    note: Optional[str] = None
    min_threshold: Optional[int] = 1

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    barcode: Optional[str] = None
    note: Optional[str] = None
    min_threshold: Optional[int] = None

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True

class ItemDetail(Item):
    current_quantity: Optional[int] = None
    category: Optional[Category] = None

# 在庫関連のスキーマ
class StockBase(BaseModel):
    item_id: int
    quantity: int
    location: Optional[str] = None

class StockCreate(StockBase):
    pass

class StockUpdate(BaseModel):
    quantity: Optional[int] = None
    location: Optional[str] = None

class Stock(StockBase):
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True

class StockDetail(Stock):
    item: ItemDetail
    
    class Config:
        from_attributes = True
        orm_mode = True 