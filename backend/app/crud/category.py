from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from app.models.category import Category

# ロガー設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# カテゴリの取得（全件）
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Category]:
    try:
        logger.info(f"カテゴリ取得開始: skip={skip}, limit={limit}")
        query = select(Category).offset(skip).limit(limit)
        result = await db.execute(query)
        categories = result.scalars().all()
        logger.info(f"カテゴリ取得完了: {len(categories)}件")
        return categories
    except Exception as e:
        logger.error(f"カテゴリ取得中にエラー発生: {str(e)}")
        raise

# カテゴリ名でカテゴリを取得
async def get_category_by_name(db: AsyncSession, name: str) -> Optional[Category]:
    query = select(Category).where(Category.name == name)
    result = await db.execute(query)
    return result.scalars().first()
