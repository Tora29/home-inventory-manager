from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base import Base

class Item(Base):
    """アイテムモデル"""
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String(13), nullable=True, unique=True)
    name = Column(String(100), nullable=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    min_threshold = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # リレーションシップ
    stocks = relationship("Stock", back_populates="item")
    category = relationship("Category", back_populates="items") 