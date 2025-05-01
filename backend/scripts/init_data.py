# docker compose exec backend bash
# alembic revision --autogenerate -m "add comment"
# alembic upgrade head

# docker compose exec backend python -m scripts.init_data
# 初期データを投入する

# docker compose exec db psql -U postgres -d inventory_db

import sys
import os
import asyncio

from sqlalchemy import delete

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from app.db.session import SessionLocal
from app.models.location import Location
from app.models.category import Category
from app.models.item import Item
from app.models.stock import Stock

async def init():
    async with SessionLocal() as db:
        await db.execute(delete(Stock))
        await db.execute(delete(Item))
        await db.execute(delete(Category))
        await db.execute(delete(Location)) 
        await db.commit()


    # データ作成
    locations = [
        Location(name="キッチン"),
        Location(name="リビング"),
        Location(name="寝室"),
        Location(name="玄関"),
        Location(name="トイレ")
    ]
    categories = [
        Category(name="日用品"),
        Category(name="食品"),
    ]
    items = [
        Item(barcode="1234567890123", name="トイレットペーパー", min_threshold=2, category=categories[0]),
        Item(barcode="1234567890124", name="お米", min_threshold=1, category=categories[1]),
    ]
    stocks = [
        Stock(item=items[0], location=locations[0], quantity=10),
        Stock(item=items[1], location=locations[1], quantity=5),
    ]

    db.add_all(locations + categories + items + stocks)
    await db.commit()
    print("✅ 初期データを投入しました")

if __name__ == "__main__":
    asyncio.run(init())
