from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    value: str

class ItemAddOrUpdate(BaseModel):
    id: int
    name: str
    value: str

class ItemDelete(BaseModel):
    id: int

class ItemUpdate(BaseModel):
    id: int
    name: str
    value: str

class ItemResponse(BaseModel):
    id: int
    name: str
    value: str
