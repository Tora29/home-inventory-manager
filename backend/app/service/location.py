from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.location import Location

# すべての部屋を取得
async def get_locations(db: AsyncSession) -> List[Location]:
    """すべてのロケーションを取得する"""
    query = select(Location)
    result = await db.execute(query)
    locations = result.scalars().all()
    return locations