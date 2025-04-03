from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.db.database import get_db
from app.crud import stock as stock_crud
from app.crud import item as item_crud
from app.models.schemas import StockDetail, BarcodeStockIn, StockInResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# WebSocket接続を管理するクラス
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"新しいWebSocket接続: 現在の接続数 {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket接続切断: 残り接続数 {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"WebSocket送信エラー: {e}")

# WebSocket接続マネージャのインスタンス作成
manager = ConnectionManager()

@router.get("/stocks/", response_model=List[StockDetail])
async def read_stocks(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """
    すべての在庫情報を取得します。
    """
    stocks = await stock_crud.get_stocks(db, skip=skip, limit=limit)
    return stocks

@router.post("/stock/in", response_model=StockInResponse)
async def create_stock_from_barcode(
    barcode_data: BarcodeStockIn,
    db: AsyncSession = Depends(get_db)
):
    """
    バーコードスキャンから商品を入荷処理します。
    
    - バーコードに対応する商品を探し、在庫を追加します
    - 既存の在庫があれば数量を増やし、なければ新規作成します
    - WebSocketを通じて入荷通知を送信します
    """
    logger.info(f"バーコード入荷処理: {barcode_data.barcode}")
    
    try:
        # 商品が存在するか確認
        item = await item_crud.get_item_by_barcode(db, barcode_data.barcode)
        
        if not item:
            logger.warning(f"商品が見つかりません: バーコード {barcode_data.barcode}")
            return StockInResponse(
                success=False,
                message=f"バーコード {barcode_data.barcode} に対応する商品が見つかりません"
            )
        
        # 在庫追加処理
        stock = await stock_crud.add_stock_by_barcode(
            db, 
            barcode_data.barcode, 
            barcode_data.location, 
            barcode_data.quantity
        )
        
        if not stock:
            return StockInResponse(
                success=False,
                message="在庫の更新に失敗しました"
            )
        
        # 詳細な在庫情報を取得
        stocks = await stock_crud.get_stocks(db)
        stock_detail = None
        for s in stocks:
            if s.id == stock.id:
                stock_detail = s
                break
        
        # WebSocketを通じて通知
        notification = {
            "type": "stock_in",
            "data": {
                "item_id": item.id,
                "item_name": item.name,
                "barcode": item.barcode,
                "location": barcode_data.location,
                "quantity": barcode_data.quantity,
                "total_quantity": stock.quantity,
                "category_id": item.category_id,
                "category_name": item.category.name if item.category else "未分類"
            }
        }
        
        # ログに詳細情報を出力して調査
        logger.info(f"通知データ: item_name={item.name}, barcode={item.barcode}, quantity={barcode_data.quantity}, total_quantity={stock.quantity}, category_id={item.category_id}, category_name={item.category.name if item.category else '未分類'}")
        
        await manager.broadcast(notification)
        
        return StockInResponse(
            success=True,
            message=f"{item.name} を {barcode_data.quantity} 個入荷しました",
            stock=stock_detail,
            item_name=item.name
        )
        
    except Exception as e:
        logger.error(f"入荷処理中にエラー発生: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        return StockInResponse(
            success=False,
            message=f"エラーが発生しました: {str(e)}"
        )

@router.websocket("/ws/stock")
async def websocket_endpoint(websocket: WebSocket):
    """
    在庫更新の通知を受け取るためのWebSocketエンドポイント
    """
    await manager.connect(websocket)
    try:
        while True:
            # クライアントからのメッセージを待機
            # 今回は特に何もしない（バーコードスキャンのみ）
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)