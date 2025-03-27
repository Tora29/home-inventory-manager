from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.endpoints import root, items, categories, inventory, transactions
from app.db.database import engine

# 全モデルを明示的にインポートしてSQLAlchemyに認識させる
from app.models.item import Item
from app.models.category import Category
from app.models.inventory import Inventory
from app.models.transaction import Transaction

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    yield
    
    # シャットダウン処理
    await engine.dispose()

app = FastAPI(
    title="Home Inventory Manager",
    description="API for managing home inventory",
    version="0.1.0",
    lifespan=lifespan,
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://100.64.1.15:8080", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_path = "/v1"

# エンドポイントルーターをアプリケーションに登録
app.include_router(root.router, prefix=f"{base_path}", tags=["root"])
app.include_router(items.router, prefix=f"{base_path}", tags=["items"])
app.include_router(categories.router, prefix=f"{base_path}", tags=["categories"])
app.include_router(inventory.router, prefix=f"{base_path}", tags=["inventory"])
app.include_router(transactions.router, prefix=f"{base_path}", tags=["transactions"])
