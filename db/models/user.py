### Clase usuario de negocio ###

from pydantic import BaseModel, Field   # Permite crear una Entidad
from typing import Optional
from bson import ObjectId

class User_db(BaseModel):
    _id: Optional[ObjectId] = None
    login: str
    password: Optional[str] = None
    enabled: int
    
class User_business(BaseModel):
    id: str
    login: str
    password: Optional[str] = None
    enabled: int        