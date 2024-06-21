### CUENTAS DB API ###
from fastapi import APIRouter, HTTPException, status
from db.models.account import Account
from db.client import db_client
from bson import ObjectId

router = APIRouter(
    prefix='/accounts',
    tags=["Cuentas"],
    responses={status.HTTP_404_NOT_FOUND: {'message':"No encontrado"}}
)


"""
    API: Consular las Cuentas de un cliente
    wlopera
    @Jun 2024
"""
@router.get('/{id}', response_model=Account)
async def getAccount(id:str):
    cursor = db_client.accounts.find_one({"_id": ObjectId(id)})
    return create_account(cursor)


"""
    API: Agregar un cuenta
    wlopera
    @Jun 2024
"""
@router.post('/add/', response_model=Account, status_code=status.HTTP_201_CREATED )
async def addAccount(account_data: Account, client_id: str):
    try: 
        account = dict(account_data)
        del account['id']
        del account['transactions']
        account_id = db_client.accounts.insert_one(account).inserted_id
        db_client.clients.update_one(
            {'_id': ObjectId(client_id)},
            {'$push': {'accounts': account_id}}
        )       
        return await getAccount(account_id)
    except Exception as e:
        print(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)})
    

"""
    API: Modificar la cuenta
    wlopera
    @Jun 2024
"""
@router.put('/modify/', response_model=Account)
async def modifyClient(account:Account):
    try:  
        update_data = {
            "balance": account.balance,
            "idTypeAccount": account.idTypeAccount,    
            "transactions": account.transactions,
            "date": account.date
        }
        
        response = db_client.accounts.update_one({"_id": ObjectId(account.id)},  {"$set": update_data}) 
        # Validar si se realizo el cambio
        if response.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": str("No se ha actualizado la cuenta")})
        else:
            return await getAccount(account.id)
    except HTTPException as http_exception:
        print(f"Excepción manejada: {http_exception}")
        raise http_exception
    except Exception as e:
        print(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)})


"""
    API: Eliminar un cuenta
    wlopera
    @Jun 2024
"""
@router.delete('/delete/{client_id}/{account_id}/', response_model=dict)
async def deleteAccount(client_id:str, account_id: str): 
    try: 
        deleted_account = db_client.accounts.delete_one({"_id": ObjectId(account_id)}).deleted_count

        # Validar si se elimino la cuenta
        if deleted_account == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": str("No se ha eliminado la cuenta")})
        else:
            db_client.clients.update_one(
            {'_id': ObjectId(client_id)},
            {'$pull': {'accounts': ObjectId(account_id)}}
        )    
            return {"message": f"Cuenta {account_id} eliminada"}
    except Exception as e:
        print(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)})
    
    
"""
    Crear objeto cuentas
    cursor(Account_db): Datos de la cuenta de base de datos
    wlopera
    @Jun 2024
    return  Datos de la cuenta del cliente (negocio)
"""
def create_account(cursor):
    cursor["id"] = str(cursor["_id"])
    del cursor["_id"]   
    return Account(**cursor)

        
