from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class TodoList(Base):
    __tablename__ = "todolists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    items = relationship("Item", back_populates="todolist", cascade="all, delete")
