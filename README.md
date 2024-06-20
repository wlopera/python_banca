## PROYECTO BANCA PYTHON, REACT Y REACT NATIVE

Proyecto de estudio de un Banco que permite conectarse como administrador y generar usuarios, cuentas y transacciones y como usuario permite conectarse, consultar cuentas y realizar transacciones (Pagos y transferencias bancarias).

ver: doc/Proyecto-banca-backend.docx

ver Proyecto recat-banca: https://github.com/wlopera/react_banca

* Python: APIs de servicios
    *  Usuarios
    *  Clientes
    *  Cuentas
    *  Tipos
    *  Transacciones
    *  Tipo de transacciones
    *  
![image](https://github.com/wlopera/python_banca/assets/7141537/fa8cfd9b-7f87-49b7-845d-4d6b89c80e6e)
Nota: MondoDB

* React: Web del banco
    *  Admin:  administrar usuarios y cuentas 
    *  Usuarios: Consulta y transacciones bancarias

![image](https://github.com/wlopera/python_banca/assets/7141537/3df166a1-92bd-4741-a49f-0201a6cfb127)

* React Native: Consulta y transacciones bancarias solo para usuarios
  
![image](https://github.com/wlopera/python_banca/assets/7141537/ce07cbf1-8a76-4877-9158-2d2594132d4a)

## Python

Desarrollo de API de usuarios que permiten ingresar a la banca. Inicialmente se va a permitir el acceso pero luego se debe generar token y validaciones de seguridad.

Librerías requeridas:
* FastApi 		(fastapi)
* APIRouter 		(fastapi)
* HTTPException	(fastapi)
* BaseModel 	(pydantic)
* pymongo		(MongoClient)
* uvicorn                      Para levantar el servidor de python

* pip install fastapi
  https://pypi.org/project/fastapi/
  https://fastapi.tiangolo.com/es/

* pip install "uvicorn[standard]"
  https://pypi.org/project/uvicorn/
  https://pywombat.com/articles/introduccion-pydantic

### Para levantar servidor
![image](https://github.com/wlopera/python_banca/assets/7141537/ab3bc810-a56d-4346-aef5-a2ab6d1827ce)

pip install pymongo
  https://pypi.org/project/pymongo/


### Extensiones o plugin para VSCODE
THUNDER CLINT	Cliente para consumo de servicios API
Python
Python Extension Pack

### Probar Servidor de Python
```
from fastapi import FastAPI

app = FastAPI()
@app.get('/')
async def getUser():
    return {
        'id':"AQSWDE12345FRGTFG654646",
        'login':"wlopera",
        'password': "*****",
        'enabled': 1
    }
```

### Levantar y probar servicio
PS C:\A_CURSOS\2024\Proyecto\Backend> uvicorn main:app --reload
![image](https://github.com/wlopera/python_banca/assets/7141537/a6980a95-ad07-4acd-bc72-77038ddf1e78)

Agregar route para manejo de varios APIS. Route API users

#### users.py
```
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                   tags=["Usuarios"],
                   responses={404: {'message':"No Encontrado"}})
#Clase Usuario
    
class User(BaseModel):
    id: str
    login:str
    password:str
    enable: int
    
#Lista de Usuario
users_list =[User(id="aqswe12345", login="lmessi",password="11111",enable=1),
             User(id="q1w2e3r4t5", login="cr7",password="22222",enable=1),
             User(id="f5g3h6j7hh", login="njunior",password="33333",enable=1),
             User(id="e3r4tf6ytf", login="lsuarez",password="44444",enable=0),
             User(id="98765fgdrs", login="jarango",password="55555",enable=1)]
#Consultar usuarios
@router.get("/")
async def users():
    return users_list
```

### main.py
```
from fastapi import FastAPI
from routers import users

app = FastAPI()

#Routers
app.include_router(users.router)
```

### Salida
![image](https://github.com/wlopera/python_banca/assets/7141537/1183a7ed-5d1d-44fb-8e1a-ed886ca9eeb8)

Uso de MongoDB

* Instalar MongoDB y Herramientas de MongoDB:
  https://www.mongodb.com/docs/manual/installation
  https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows

* gregar MongoDb al path

* Crear carpetas para db y log:
 	- C:\A_CURSOS\2024\Proyecto\Backend\data\db
  - C:\A_CURSOS\2024\Proyecto\Backend\data\log

*Crear archivo para levantar MongoDB:
- C:\A_CURSOS\2024\Proyecto\Backend\data\mongod.cfg
```
storage:
dbPath: C:\A_CURSOS\2024\Proyecto\Backend\data\db
#Descomentar si quiero crear archivo de log:
#systemLog:
  #destination: file
#path: C:\A_CURSOS\2024\Proyecto\Backend\data\logs\mongod.log
#logAppend: true
net:
  bindIp: 127.0.0.1
  port: 27017
```
  
### Levantar MongoDB
    C:\A_CURSOS\2024\Proyecto\Backend\data> mongod --config mongod.cfg
    ó
    C:\A_CURSOS\2024\Proyecto\Backend\data> mongod --dbpath "C:\A_CURSOS\2024\Proyecto\Backend\data\db"

    Conexión: mongod://localhost  [url:port]
    
![image](https://github.com/wlopera/python_banca/assets/7141537/0a585c18-404a-4bce-b6ec-62f02466dbac)


Se crear el archivo de mongo en la ruta definida en el archivo config mongod.cfg
![image](https://github.com/wlopera/python_banca/assets/7141537/c96b4135-7ea1-40c1-9e03-453bc71898e4)


#### Instalar Plugin MongoDB en Vscode

Conectar a MongoDB desde el plugin:
    > mongodb://localhost:27017
        localhost:
            admin
            config
            local

![image](https://github.com/wlopera/python_banca/assets/7141537/025ce1fa-5c5a-4fd2-9f38-9eb17cffc1ff)

* Conexio a MongoDB Atlas
- Crear Projecto en Mongo Atlas
- Crear DB an Mongo Atlas.

* Conectarse a Mongo Atlas desde VSCODE
    	_> mongodb+srv://admin:<password>@cluster0.gioxlj8.mongodb.net/
       	_>mongodb+srv://admin:admin@cluster0.gioxlj8.mongodb.net/

 *Conectarse a Mongo Atlas desde Pyhton - 3.12+:
    _> mongodb+srv://admin:<password>@cluster0.gioxlj8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
    _> mongodb+srv://admin:admin@cluster0.gioxlj8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

* Codigo de Ejemplo:
```
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi
    uri = "mongodb+srv://admin:<password>@cluster0.gioxlj8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
```


#### Crear API de Usuarios conectado a MongoDB users_db.py
![image](https://github.com/wlopera/python_banca/assets/7141537/d83df093-e4ce-4345-a549-c2514de574da)

#### Esquemas: 
```
def user_schemas(user) -> dict:
    return {
        "id": str(user["_id"]),
        "login": user["login"],
        "password": user["password"],
        "enable": user["enable"]    
    }
    
def users_schemas(users) -> list:
    return [user_schemas(user) for user in users]
```

#### Modelo:
```
### Clase usuario de negocio ###
from pydantic import BaseModel   # Permite crear una Entidad
from typing import Optional
class User(BaseModel):
    id: Optional[str] = None # Implica que es opcional
    login: str
    password: str
    enable: int
```

#### Cliente:
```
from pymongo import MongoClient
# Conexion a DB local (localhost)
db_client = MongoClient().local
```

#### API
```
### USER DB API ###
from fastapi import APIRouter
from db.models.user import User
from db.schemas.user import user_schemas, users_schemas
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/users",
                   tags=["Usuarios"],
                   responses={404: {'message':"No Encontrado"}})
# API Consulta de usuarios
@router.get("/", response_model=list[User])
async def users():
    return users_schemas(db_client.users.find())
```

Data cargada como dummy en la DB de mongo:
![image](https://github.com/wlopera/python_banca/assets/7141537/a98e753b-2df6-458c-bf21-9351002f69c3)

#### Salida:
![image](https://github.com/wlopera/python_banca/assets/7141537/cf8266df-2bd8-46b3-be30-c8a3789b9a88)



Consultas de MongoDB en Python. Algunas páginas de ayuda
https://www.w3schools.com/python/python_mongodb_find.asp
https://www.w3schools.com/python/python_mongodb_query.asp

user-db.py
```
...
class UserLogin(BaseModel):
    login: str
password: str
...
# API Consulta de usuario por login
@router.get("/login/", response_model=User)
async def user(userLogin:UserLogin):
return user_schemas(db_client.users.find_one({'login':userLogin.login}))
...
```

#### Ver API vía web por Swagger
![image](https://github.com/wlopera/python_banca/assets/7141537/bd753b14-8e94-4039-9959-f99399ee69cb)
![image](https://github.com/wlopera/python_banca/assets/7141537/ea0dee16-f8af-47da-a543-d3cd1da8a67e)


#### Salida
![image](https://github.com/wlopera/python_banca/assets/7141537/5d4e63e3-32c7-44ad-8563-fee66f617df5)


### Código:


#### Clase Usuario
```
### Clase usuario de negocio ###

from pydantic import BaseModel, Field   # Permite crear una Entidad
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
```


#### Esquema usuario
```
# Esquema de la DB User
def user_schema(user, field) -> dict:
    return {
        field: str(user[field]),
        "login": user["login"],
        "password": user["password"],
        "enabled": user["enabled"]    
    }
       
def users_schema(users, field) -> list:
    return [user_schema(user, field) for user in users]
```


#### Route usuarios
```
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
@router.put("/enabled/",  response_model=User_business)
async def setEnabled(user_business:User_business):
    try:
        update_data = {
            'enabled': user_business.enabled
        }   
        db_client.users.update_one({"_id": ObjectId(user_business.id)},  {"$set": update_data})
        return user_business
    except:
        return "No se ha actualizado el estado del usuario"

    
# API modificar password
@router.put("/password/",  response_model=User_business)
async def setPassword(user_business:User_business):
    try:
        update_data = {
            'password': user_business.password
        } 
        
        db_client.users.update_one({"_id": ObjectId(user_business.id)},  {"$set": update_data})
        return user_business
    except:
        return "No se ha actualizado el password"  

# Crear usuario
@router.post("/add/", response_model= User_business, status_code=status.HTTP_201_CREATED )
async def add_user(user:User_db):
    if type(search_user("login", user.login)) == User_db:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe") 
    else:
           
        # Crear usuario DB y convertir a Json
        user_db = User_db(login=user.login, password =user.password, enabled=user.enabled)

        # Esquema de usuario - generar usuario y obtener el id generado en mongoDB
        id = db_client.users.insert_one(dict(user)).inserted_id
    
        # Consultar el usuario generado, directamente en mongoDB (_id es como lo genera mongoDB)
        new_user = db_client.users.find_one({"_id": id})

        # Generar el objeto User de la respuesta del schema
        return convert_to_user_business(new_user)
        
            
# Funcion para consultar un usuario por campo generico
def search_user(field: str, key):    
    try:
        user_db = db_client.users.find_one({field: key})        
        return user_db
    except:
        return {"error": "No se encontro usuario"}
    
    
# Función para convertir de User_db a User_business
def convert_to_user_business(user_db):
    return User_business(
        id=str(user_db['_id']),
        login=user_db['login'],
        # Comentar para no enviar al frontend
        password=user_db['password'],
        enabled=user_db['enabled']
    )
```

### Salida

#### Consultar Usuarios
![image](https://github.com/wlopera/python_banca/assets/7141537/d3087f39-5e67-4220-8d2a-170d9d55a2be)

### Crear Usuario
![image](https://github.com/wlopera/python_banca/assets/7141537/e6958121-0dc9-4acb-934b-60622aa07cd7)

![image](https://github.com/wlopera/python_banca/assets/7141537/f952c3f5-6bf8-424c-a778-704cf40b7039)



