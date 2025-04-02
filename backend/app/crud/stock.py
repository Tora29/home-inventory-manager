from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import contains_eager
import logging

from app.models.stock import Stock
from app.models.item import Item

# ロガー設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 在庫の取得（全件）
async def get_stocks(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Stock]:
    try:
        logger.info(f"在庫データ取得開始: skip={skip}, limit={limit}")
        query = (
            select(Stock)
            .join(Stock.item)
            .options(
                contains_eager(Stock.item).joinedload(Item.category)
            )
            .offset(skip)
            .limit(limit)
        )
        
        result = await db.execute(query)
        stocks = result.unique().scalars().all()
        
        # デバッグ出力
        logger.info(f"取得した在庫数: {len(stocks)}")
        for stock in stocks:
            category_name = stock.item.category.name if stock.item and stock.item.category else "None"
            logger.debug(f"Stock ID: {stock.id}, Item: {stock.item.name}, Category: {category_name}")
            
        return stocks
    except Exception as e:
        logger.error(f"在庫データ取得中にエラー発生: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise

# アイテムIDと場所で在庫を取得
async def get_stock_by_item_id_and_location(
    db: AsyncSession, item_id: int, location: str
) -> Optional[Stock]:
    query = select(Stock).where(
        Stock.item_id == item_id,
        Stock.location == location
    )
    result = await db.execute(query)
    return result.scalars().first()
