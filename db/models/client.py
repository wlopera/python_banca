### Clase cliente de negocio ###

from pydantic import BaseModel
from typing import Optional, List
from db.models.account import Account
            
"""
    Clase: Clientes simple (con id de las cuentas)
    wlopera
    @Jun 2024
"""         
class Client(BaseModel):
    id: Optional[str] = None
    identification: str
    name: str
    email:str
    phone: str
    accounts: Optional[List[str]] = None
    
    
"""
    Clase: Clientes completos (con datos de las cuentas)
    wlopera
    @Jun 2024
"""     
class Client_full(BaseModel):
    id: str
    identification: str
    name: str
    email:str
    phone: str
    accounts: Optional[List[Account]] = None    

