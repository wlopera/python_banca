### Clase usuario de negocio ###

from pydantic import BaseModel   # Permite crear una Entidad
from typing import Optional

class User_db(BaseModel):
    id: Optional[str] = None # Implica que es opcional
    login: str
    password: str
    enabled: int
    
class User(BaseModel):
    login: str
    enabled: int    