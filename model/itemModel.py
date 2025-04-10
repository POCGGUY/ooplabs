from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    text = Column(String, nullable=True)
    is_done = Column(Boolean, default=False)

    todolist_id = Column(Integer, ForeignKey("todolists.id", ondelete="CASCADE"))
    todolist = relationship("TodoList", back_populates="items")
