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

# バーコードスキャンで商品を追加（在庫の増加）
async def add_stock_by_barcode(
    db: AsyncSession, barcode: str, location: str = "入荷", quantity: int = 1
) -> Optional[Stock]:
    """
    バーコードから商品を検索し、在庫を追加します。
    既存の在庫があれば数量を増やし、なければ新しい在庫レコードを作成します。
    
    Args:
        db: データベースセッション
        barcode: 商品バーコード
        location: 保管場所 (デフォルト: "入荷")
        quantity: 追加数量 (デフォルト: 1)
        
    Returns:
        更新または作成された在庫オブジェクト、商品が見つからない場合はNone
    """
    from app.crud.item import get_item_by_barcode
    
    try:
        logger.info(f"在庫追加処理開始: バーコード={barcode}, 場所={location}, 数量={quantity}")
        
        # バーコードから商品を検索
        item = await get_item_by_barcode(db, barcode)
        if not item:
            logger.warning(f"商品が見つかりません: バーコード={barcode}")
            return None
            
        logger.info(f"商品を検出: ID={item.id}, 名前={item.name}")
        
        # 既存の在庫を検索
        stock = await get_stock_by_item_id_and_location(db, item.id, location)
        
        if stock:
            # 既存の在庫がある場合は数量を増やす
            logger.info(f"既存の在庫を更新: 現在数量={stock.quantity} -> {stock.quantity + quantity}")
            stock.quantity += quantity
        else:
            # 新しい在庫レコードを作成
            logger.info(f"新しい在庫を作成: アイテムID={item.id}, 場所={location}, 数量={quantity}")
            stock = Stock(
                item_id=item.id,
                location=location,
                quantity=quantity
            )
            db.add(stock)
            
        # 変更をコミット
        await db.commit()
        # リフレッシュして最新の状態を取得
        await db.refresh(stock)
        
        logger.info(f"在庫追加処理完了: 在庫ID={stock.id}, 現在数量={stock.quantity}")
        return stock
        
    except Exception as e:
        # エラー発生時はロールバック
        await db.rollback()
        logger.error(f"在庫追加中にエラー発生: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise
