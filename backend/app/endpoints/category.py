from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.crud import category as category_crud
from app.models.schemas import Category

router = APIRouter()

@router.get("/categories/", response_model=List[Category])
async def read_categories(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """
    すべてのカテゴリを取得します。
    """
    categories = await category_crud.get_categories(db, skip=skip, limit=limit)
    return categories