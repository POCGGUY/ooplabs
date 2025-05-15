from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from config.database import Base
import datetime

class TodoList(Base):
    __tablename__ = "todolists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    completed_count = Column(Integer, default=0)
    total_count = Column(Integer, default=0)
    items = relationship( "Item", back_populates="todolist", cascade="all, delete-orphan", lazy="selectin")
