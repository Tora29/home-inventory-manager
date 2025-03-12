from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

# 環境変数からデータベースURLを取得
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/inventory_db")

# 非同期エンジンの作成
engine = create_async_engine(DATABASE_URL, echo=True)

# 非同期セッションの作成
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 依存性として使用するデータベースセッションの取得関数
async def get_db():
    """
    データベースセッションを提供する依存性関数
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 