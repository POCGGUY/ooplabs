from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    text: str | None = None
    is_done: bool = False


class ItemCreate(ItemBase):
    todolist_id: int


class ItemUpdate(BaseModel):
    name: str | None = None
    text: str | None = None
    is_done: bool | None = None


class ItemRead(ItemBase):
    id: int
    todolist_id: int

    class Config:
        orm_mode = True
