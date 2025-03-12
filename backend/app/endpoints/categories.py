from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.crud import category as category_crud
from app.models.schemas import Category, CategoryCreate, CategoryUpdate

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

@router.get("/categories/{category_id}", response_model=Category)
async def read_category(
    category_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDのカテゴリを取得します。
    """
    db_category = await category_crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.post("/categories/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    新しいカテゴリを作成します。
    """
    return await category_crud.create_category(db=db, category=category)

@router.put("/categories/{category_id}", response_model=Category)
async def update_category(
    category_id: int, 
    category: CategoryUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDのカテゴリを更新します。
    """
    db_category = await category_crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    updated_category = await category_crud.update_category(db=db, category_id=category_id, category=category)
    return updated_category

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDのカテゴリを削除します。
    """
    db_category = await category_crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    success = await category_crud.delete_category(db=db, category_id=category_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete category")
    
    return None 