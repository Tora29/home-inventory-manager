from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base import Base

class Room(Base):
    """部屋モデル"""
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # リレーションシップ
    stocks = relationship("Stock", back_populates="room") 