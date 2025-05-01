from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.service import category as category_crud
from app.schemas import Category

router = APIRouter()

@router.get("/categories/", response_model=List[Category])
async def read_categories(
    db: AsyncSession = Depends(get_db)
):
    """
    すべてのカテゴリを取得します。
    """
    categories = await category_crud.get_categories(db)
    return categories