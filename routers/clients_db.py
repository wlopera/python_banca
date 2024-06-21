### CLIENTES DB API ###
from fastapi import APIRouter, HTTPException, status
from db.models.client import Client, Client_full
from db.models.account import Account
from db.client import db_client
from bson import ObjectId

router = APIRouter(
    prefix='/clients',
    tags=["Clientes"],
    responses={status.HTTP_404_NOT_FOUND: {'message':"No encontrado"}}
)


"""
    API: Consultar Clientes simple (con id de las cuentas)
    wlopera
    @Jun 2024
"""
@router.get('/', response_model=list[Client])
async def getClients():
    cursors_client = db_client.clients.find()
    clients = []
    for cursor_client in cursors_client:   
        accounts = []
        for account_id in cursor_client.get('accounts', []):
            accounts.append(str(account_id))               
        clients.append(create_client(cursor_client, accounts))
        
    return clients


"""
    API: Consultar Clientes completa (con datos de las cuentas)
    wlopera
    @Jun 2024
"""
@router.get('/full/', response_model=list[Client_full])
async def getClientsFull():
    cursors_client = db_client.clients.find()
    clients = []
    for cursor_client in cursors_client:
        accounts = []
        for account_id in cursor_client.get('accounts', []):
            cursor_account = db_client.accounts.find_one({"_id":ObjectId(account_id)})
            accounts.append(create_account(cursor_account))
        clients.append(create_client_full(cursor_client, accounts)) 
        
    return clients


    # cursors = db_client.clients.find()
    # clients = []
    # for cursor in cursors:   
    #     accounts = []
    #     for account_id in cursor.get('accounts', []):
    #         accounts.append(str(account_id))               
    #     clients.append(create_client(cursor, accounts))

"""
    API: Consultar un cliente (con id de las cuentas)
    wlopera
    @Jun 2024
"""
@router.get('/{id}/', response_model=Client)
async def getClient(id:str):   
    cursor = db_client.clients.find_one({"_id":ObjectId(id)})
    accounts = []
    for account_id in cursor.get('accounts', []):
        accounts.append(str(account_id))               
    return create_client(cursor, accounts)


"""
    API: Agregar un cliente (sin datos de las cuentas)
    wlopera
    @Jun 2024
"""
@router.post('/add/', response_model=Client, status_code=status.HTTP_201_CREATED )
async def addClient(client:Client):
    try: 
        new_client = dict(client)
        del new_client['id']
        del new_client['accounts']
        id = db_client.clients.insert_one(new_client).inserted_id
        return await getClient(id)
    except Exception as e:
        print(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)})
    

"""
    API: Modificar al cliente (solo el cliente, no sus cuentas)
    wlopera
    @Jun 2024
"""
@router.put('/modify/', response_model=Client)
async def modifyClient(client:Client):
    try:  
        update_data = {
            "identification": client.identification,
            "name": client.name,
            "email":client.email,
            "phone":client.phone
        }
        response = db_client.clients.update_one({"_id": ObjectId(client.id)},  {"$set": update_data}) 
        # Validar si se realizo el cambio
        if response.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": str("No se ha actualizado el cliente")})
        else:
            return await getClient(client.id)
    except HTTPException as http_exception:
        print(f"Excepción manejada: {http_exception}")
        raise http_exception
    except Exception as e:
        print(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)})


"""
    API: Eliminar un cliente
    wlopera
    @Jun 2024
"""
@router.delete('/delete/{id}', response_model=dict)
async def deleteClient(id:str):
    try: 
        deleted_count = db_client.clients.delete_one({"_id": ObjectId(id)}).deleted_count

        # Validar si se elimino el cliente
        if deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": str("No se ha eliminado el cliente")})
        else:
            return {"message": f"Cliente {id} eliminado"}
    except Exception as e:
        print(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)})
    
    
"""
    Metodo: Crear objeto cliente simple
    cursor(Client_db): Datos del cliente de base de datos
    @accounts(list[str]): Lista de id de cuentas del cliente (negocio)
    wlopera
    @Jun 2024
    return  Datos simple del cliente (negocio)
"""
def create_client(cursor, accounts):
    cursor["id"] = str(cursor["_id"])
    cursor["accounts"] = accounts
    del cursor["_id"]   
    return Client(**cursor)

"""
    Meotodo: Crear objeto cliente completa
    cursor(Client_db): Datos del cliente de base de datos
    @accounts(list[Account]): Lista de  cuentas del cliente (negocio)
    wlopera
    @Jun 2024
    return  Datos completos del cliente (negocio)
"""
def create_client_full(cursor, accounts):
    cursor["id"] = str(cursor["_id"])
    cursor["accounts"] = accounts
    del cursor["_id"]   
    return Client_full(**cursor)

    
    
"""
    Crear objeto cuentas
    account_db(Account_db): Datos de la cuenta de base de datos
    wlopera
    @Jun 2024
    return  Datos de la cuenta del cliente (negocio)
"""
def create_account(cursor):
    cursor["id"] = str(cursor["_id"])
    del cursor["_id"]   
    return Account(**cursor)
        
