from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Rank(Base):
    __tablename__ = "ranks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    position = Column(Integer)
    values = relationship("Value", back_populates="rank")

class Pillar(Base):
    __tablename__ = "pillars"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    position = Column(Integer)
    color_bg = Column(String)
    color_text = Column(String)
    items = relationship("Item", back_populates="pillar", cascade="all, delete-orphan")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    pillar_id = Column(Integer, ForeignKey("pillars.id"))
    pillar = relationship("Pillar", back_populates="items")
    values = relationship("Value", back_populates="item", cascade="all, delete-orphan")

class Value(Base):
    __tablename__ = "values"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    item_id = Column(Integer, ForeignKey("items.id"))
    rank_id = Column(Integer, ForeignKey("ranks.id"))
    item = relationship("Item", back_populates="values")
    rank = relationship("Rank", back_populates="values")