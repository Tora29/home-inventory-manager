from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import uvicorn

from app.endpoints import root, stock, category, item, room

from app.db.database import engine

from app.models.item import Item
from app.models.stock import Stock
from app.models.category import Category
from app.models.room import Room

# 環境変数の読み込み
load_dotenv()

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
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:8080").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_path = "/v1"

# エンドポイントルーターをアプリケーションに登録
app.include_router(root.router, prefix=f"{base_path}", tags=["root"])
app.include_router(item.router, prefix=f"{base_path}", tags=["items"])
app.include_router(stock.router, prefix=f"{base_path}", tags=["stocks"])
app.include_router(category.router, prefix=f"{base_path}", tags=["categories"])
app.include_router(room.router, prefix=f"{base_path}", tags=["rooms"])
# app.include_router(websocket.router, prefix=f"{base_path}", tags=["WebSocket"])
