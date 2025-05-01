from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.category import Category

# カテゴリの取得（全件）
async def get_categories(db: AsyncSession) -> List[Category]:
    """すべてのカテゴリを取得する"""
    query = select(Category)
    result = await db.execute(query)
    categories = result.scalars().all()
    return categories   
