from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sql_update

from app.models.room import Room
from app.models.schemas import RoomCreate, RoomUpdate

# すべての部屋を取得
async def get_rooms(db: AsyncSession) -> List[Room]:
    """すべての部屋を取得する"""
    result = await db.execute(select(Room))
    return result.scalars().all()

# 部屋をIDで取得
async def get_room(db: AsyncSession, room_id: int) -> Optional[Room]:
    """部屋をIDで取得する"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    return result.scalars().first()

# 部屋を名前で取得
async def get_room_by_name(db: AsyncSession, name: str) -> Optional[Room]:
    """部屋を名前で取得する"""
    result = await db.execute(select(Room).where(Room.name == name))
    return result.scalars().first()

# 部屋を作成
async def create_room(db: AsyncSession, room: RoomCreate) -> Room:
    """新しい部屋を作成する"""
    db_room = Room(**room.model_dump())
    db.add(db_room)
    await db.commit()
    await db.refresh(db_room)
    return db_room

# 部屋を更新
async def update_room(db: AsyncSession, room_id: int, room: RoomUpdate) -> Optional[Room]:
    """部屋を更新する"""
    update_data = room.model_dump(exclude_unset=True)
    if not update_data:
        return None
    
    await db.execute(
        sql_update(Room)
        .where(Room.id == room_id)
        .values(**update_data)
    )
    await db.commit()
    
    return await get_room(db, room_id)

# 部屋を削除
async def delete_room(db: AsyncSession, room_id: int) -> bool:
    """部屋を削除する"""
    room = await get_room(db, room_id)
    if not room:
        return False
    
    await db.delete(room)
    await db.commit()
    return True 