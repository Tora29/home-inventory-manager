from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.schemas import Room, RoomCreate, RoomUpdate
from app.crud import room as room_crud

router = APIRouter()

@router.get("/rooms", response_model=List[Room])
async def read_rooms(db: AsyncSession = Depends(get_db)):
    """
    すべての部屋を取得します。
    """
    rooms = await room_crud.get_rooms(db)
    return rooms

@router.get("/rooms/{room_id}", response_model=Room)
async def read_room(room_id: int, db: AsyncSession = Depends(get_db)):
    """
    特定の部屋を取得します。
    """
    db_room = await room_crud.get_room(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="部屋が見つかりません")
    return db_room

@router.post("/rooms", response_model=Room)
async def create_room(room: RoomCreate, db: AsyncSession = Depends(get_db)):
    """
    新しい部屋を作成します。
    """
    db_room = await room_crud.get_room_by_name(db, room.name)
    if db_room:
        raise HTTPException(status_code=400, detail="この部屋名は既に使用されています")
    return await room_crud.create_room(db, room)

@router.put("/rooms/{room_id}", response_model=Room)
async def update_room(room_id: int, room: RoomUpdate, db: AsyncSession = Depends(get_db)):
    """
    部屋の情報を更新します。
    """
    db_room = await room_crud.get_room(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="部屋が見つかりません")
    
    # 部屋名の重複チェック
    if room.name and room.name != db_room.name:
        existing_room = await room_crud.get_room_by_name(db, room.name)
        if existing_room:
            raise HTTPException(status_code=400, detail="この部屋名は既に使用されています")
    
    updated_room = await room_crud.update_room(db, room_id, room)
    return updated_room

@router.delete("/rooms/{room_id}", response_model=bool)
async def delete_room(room_id: int, db: AsyncSession = Depends(get_db)):
    """
    部屋を削除します。
    """
    db_room = await room_crud.get_room(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="部屋が見つかりません")
    
    # 部屋が在庫で使用されているかチェックする必要がある
    # ここに実装を追加
    
    return await room_crud.delete_room(db, room_id) 