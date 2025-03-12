#!/usr/bin/env python
import asyncio
from app.db.database import engine
from app.db.base import Base

# モデルを明示的にインポートして登録する
from app.models.item import Item
from app.models.category import Category
from app.models.inventory import Inventory
from app.models.transaction import Transaction

async def create_tables():
    print("データベーステーブルを作成します...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # 既存のテーブルをドロップ（注意：データが失われます）
        await conn.run_sync(Base.metadata.create_all)  # すべてのテーブルを作成
    print("テーブルの作成が完了しました")

if __name__ == "__main__":
    asyncio.run(create_tables()) 