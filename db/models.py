# db/models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, create_engine
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

Base = declarative_base()

class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Sample(Base):
    __tablename__ = "sample"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parent.id"))
    parent = relationship("Parent")

    json_data = Column(JSONB)
    score = Column(Float)
    title = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    pmpt = Column(String, nullable=True)
    pmpt_id = Column(Integer, default=1)
