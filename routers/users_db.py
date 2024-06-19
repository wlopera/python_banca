### USER DB API ###
from fastapi import APIRouter, HTTPException, status
from db.models.user import User_db, User_business
from db.schemas.user import user_schema, users_schema
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
@router.get("/", response_model=list[User_business])
async def users():
    users_db = users_schema(db_client.users.find(), "_id")
    users_business = [convert_to_user_business(user) for user in users_db]      
    return users_business



# API Consulta de usuario por login
@router.get("/login/", response_model=User_business)
async def user(userLogin:UserLogin):
    try:
        user_db = db_client.users.find_one({"login": userLogin.login})        
        user_bussiness = convert_to_user_business(user_db)
        return user_bussiness
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "No se encontro usuario"})


# API activar o inactivar usuario
@router.put("/enabled/",  response_model=User_business)
async def setEnabled(user_business:User_business):
    return modify_user('enabled', user_business.enabled, user_business.id, user_business, "No se ha actualizado el estado del usuario" )
    
# API modificar password
@router.put("/password/",  response_model=User_business)
async def setPassword(user_business:User_business):
     return modify_user('password', user_business.password, user_business.id, user_business, "No se ha actualizado el password del usuario" )


# API modificar tipo de usuario
@router.put("/type/",  response_model=User_business)
async def setType(user_business:User_business):
    return modify_user('type', user_business.type, user_business.id, user_business, "No se ha actualizado el tipo de usuario" )
    
    
# Crear usuario
@router.post("/add/", response_model= User_business, status_code=status.HTTP_201_CREATED )
async def add_user(user:User_db):
    if type(search_user("login", user.login)) == User_db:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "El usuario ya existe"}) 
    else:           
        # Crear usuario DB y convertir a Json
        user_db = User_db(login=user.login, password =user.password, enabled=user.enabled)

        # Esquema de usuario - generar usuario y obtener el id generado en mongoDB
        id = db_client.users.insert_one(dict(user)).inserted_id
    
        # Consultar el usuario generado, directamente en mongoDB (_id es como lo genera mongoDB)
        new_user = db_client.users.find_one({"_id": id})

        # Generar el objeto User de la respuesta del schema
        return convert_to_user_business(new_user)
        
            
# Consultar usuario por campo generico
def search_user(field: str, key):    
    try:
        user_db = db_client.users.find_one({field: key})        
        return user_db
    except:
        return {"error": "No se encontro usuario"}
    
    
# Convertir de User_db a User_business
def convert_to_user_business(user_db):
    return User_business(
        id=str(user_db['_id']),
        login=user_db['login'],
        # Comentar para no enviar al frontend
        password=user_db['password'],
        enabled=user_db['enabled'],
        type=user_db['type']
    )
    
def modify_user(key:str, value:str, id:str, user_business: User_business, message:str):
    try:        
        update_data = {
            key: value
        }
        response = db_client.users.update_one({"_id": ObjectId(id)},  {"$set": update_data})  
        
        # Validar si se realizo el cambio
        if response.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": str(message)})
        else:
            return user_business
    except HTTPException as http_exception:
        print(f"Excepción manejada: {http_exception}")
        raise http_exception
    except Exception as e:
        print(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)})