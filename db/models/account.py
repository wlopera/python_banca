### Clase cuentas de negocio ###

from pydantic import BaseModel
from typing import Optional, List

"""
    Clase: Cuentas del cliente (negocio)
    wlopera
    @Jun 2024
"""             
class Account(BaseModel):
    id: Optional[str] = None
    balance: float
    idTypeAccount: str    
    transactions: Optional[List[str]] = None
    date: str