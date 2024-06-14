### USER DB API ###
from fastapi import APIRouter, HTTPException, status
from db.models.user import User_db, User
from db.schemas.user import user_db_schema, users_db_schema, user_schema
from db.client import db_client
from bson import ObjectId
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                   tags=["Usuarios"],
                   responses={404: {'message':"No Encontrado"}})

class UserLogin(BaseModel):
    login: str
    password: str

    
# API Consulta de usuarios
@router.get("/", response_model=list[User_db])
async def users():
    return users_db_schema(db_client.users.find())


# API Consulta de usuario por login
@router.get("/login/", response_model=User)
async def user(userLogin:UserLogin):
    response  = search_user('login', userLogin.login)
    if type(response) == User:
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response)


# API activar o inactivar usuario
@router.put("/enabled/",  response_model=User_db)
async def setEnabled(user_db:User_db):
    try:
        # Creo un nuevo usuario
        modify_user = dict(user_db)
        
        # Borro el id       
        del modify_user['id']
        
        # Genero el _id
        modify_user['_id'] = ObjectId(user_db.id)
        
        db_client.users.find_one_and_replace({"_id": modify_user['_id']}, modify_user)
        return modify_user
    except:
        return "No se ha actualizado el estado del usario"

    
# API modificar password
@router.put("/password/",  response_model=User)
async def setPassword(userLogin:UserLogin):
    try:
        user_db =  db_client.users.find_one({"login": userLogin.login})     
        user_db['password'] = userLogin.password
        db_client.users.find_one_and_replace({"_id": user_db['_id']}, user_db)
        return User(**user_schema({'login':userLogin.login, 'enabled':1}))
    except:
        return "No se ha actualizado el password"  


# Crear usuario
@router.post("/add/", response_model= User, status_code=status.HTTP_201_CREATED )
async def add_user(userLogin:UserLogin):
    if type(search_user("login", userLogin.login)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe") 
    else:
        # Cerar usuario DB y convertir a Json
        user_db = dict(User_db(login=userLogin.login, password=userLogin.password, enabled=1))
        del user_db['id']

        # Esquema de usuario - generar usuario y obtener el id generado en mongoDB
        id = db_client.users.insert_one(user_db).inserted_id
    
        # Consultar el usuario generado, directamente en mongoDB (_id es como lo genera mongoDB)
        new_user = db_client.users.find_one({"_id": id})
        
        # Generar el objeto User de la respuesta del schema
        return User(**user_schema(new_user))
         
            
# Funcion para consultar un usuario por campo generico
def search_user(field: str, key):    
    try:
        user_db = db_client.users.find_one({field: key})
        del user_db['_id']
        del user_db['password']
        return User(**user_schema(user_db))
    except:
        return {"error": "No se encontro usuario"}
    
    
    