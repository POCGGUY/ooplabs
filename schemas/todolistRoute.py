from pydantic import BaseModel


class TodoListBase(BaseModel):
    name: str


class TodoListCreate(TodoListBase):
    pass


class TodoListUpdate(BaseModel):
    name: str | None = None


class TodoListRead(TodoListBase):
    id: int

    class Config:
        orm_mode = True
