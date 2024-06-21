### Clase Transacciones de negocio ###

from pydantic import BaseModel
from typing import Optional, List
        
"""
    Clase: Transacciones del cliente (negocio)
    wlopera
    @Jun 2024
"""             
class Transaction(BaseModel):
    id: Optional[str] = None
    typeTransaction: str
    description: str    
    amount: float
    date: str