### USER DB DUMMY ###
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                   tags=["Usuarios"],
                   responses={404: {'message':"No Encontrado"}})

# Clase Usuario
class User(BaseModel):
    id: str
    login:str
    password:str
    enabled: int
    
#Lista de Usuario
users_list =[User(id="aqswe12345", login="lmessi",password="11111",enabled=1),
             User(id="q1w2e3r4t5", login="cr7",password="22222",enabled=1),
             User(id="f5g3h6j7hh", login="njunior",password="33333",enabled=1),
             User(id="e3r4tf6ytf", login="lsuarez",password="44444",enabled=0),
             User(id="98765fgdrs", login="jarango",password="55555",enabled=1)]

# Consultar usuarios
@router.get("/")
async def users():
    return users_list