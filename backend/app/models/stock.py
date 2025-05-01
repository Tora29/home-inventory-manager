from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base import Base

class Stock(Base):
    """在庫モデル"""
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # リレーションシップ
    item = relationship("Item", back_populates="stocks")
    location = relationship("Location", back_populates="stocks") 