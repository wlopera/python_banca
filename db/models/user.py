### Clase usuario de negocio y usuario DB ###

from pydantic import BaseModel   # Permite crear una Entidad
from typing import Optional
from bson import ObjectId

class User_db(BaseModel):
    _id: Optional[ObjectId] = None
    login: str
    password: Optional[str] = None
    enabled: int
    type: Optional[str] = None
    
class User_business(BaseModel):
    id: str
    login: str
    password: Optional[str] = None
    enabled: int   
    type: Optional[str] = None     