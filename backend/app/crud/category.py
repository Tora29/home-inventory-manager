from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from app.models.category import Category
from app.models.schemas import CategoryCreate, CategoryUpdate

# カテゴリの取得（全件）
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Category]:
    query = select(Category).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# IDによるカテゴリの取得
async def get_category(db: AsyncSession, category_id: int) -> Optional[Category]:
    query = select(Category).where(Category.id == category_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# カテゴリの作成
async def create_category(db: AsyncSession, category: CategoryCreate) -> Category:
    db_category = Category(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

# カテゴリの更新
async def update_category(db: AsyncSession, category_id: int, category: CategoryUpdate) -> Optional[Category]:
    update_data = category.dict(exclude_unset=True)
    if not update_data:
        return None
    
    query = update(Category).where(Category.id == category_id).values(**update_data)
    await db.execute(query)
    await db.commit()
    
    return await get_category(db, category_id)

# カテゴリの削除
async def delete_category(db: AsyncSession, category_id: int) -> bool:
    query = delete(Category).where(Category.id == category_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0 