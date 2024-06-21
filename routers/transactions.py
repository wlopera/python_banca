### Transacciones DB API ###
from fastapi import APIRouter, HTTPException, status
from db.models.transaction import Transaction
from db.client import db_client
from bson import ObjectId

router = APIRouter(
    prefix='/transactions',
    tags=["Transacciones"],
    responses={status.HTTP_404_NOT_FOUND: {'message':"No encontrado"}}
)

"""
    API: Consular las transacciones de una cuenta
    wlopera
    @Jun 2024
"""
@router.get('/{id}', response_model=Transaction)
async def getTransaction(id:str):
    cursor = db_client.transactions.find_one({"_id": ObjectId(id)})
    return create_transaction(cursor)


"""
    API: Agregar un transaccion
    wlopera
    @Jun 2024
"""
@router.post('/add/', response_model=Transaction, status_code=status.HTTP_201_CREATED )
async def addTransaction(transaction_data: Transaction, account_id: str):
    try: 
        transaction = dict(transaction_data)
        del transaction['id']
        transaction_id = db_client.transactions.insert_one(transaction).inserted_id
        db_client.accounts.update_one(
            {'_id': ObjectId(account_id)},
            {'$push': {'transactions': transaction_id}}
        )       
        return await getTransaction(transaction_id)
    except Exception as e:
        print(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)})
    
"""
    API: Eliminar una transaccion
    wlopera
    @Jun 2024
"""
@router.delete('/delete/{account_id}/{transaction_id}/', response_model=dict)
async def deleteTransaction(account_id:str, transaction_id: str): 
    try: 
        deleted_transaction = db_client.transactions.delete_one({"_id": ObjectId(transaction_id)}).deleted_count

        # Validar si se elimino la transaccion
        if deleted_transaction == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": str("No se ha eliminado la transacción")})
        else:
            db_client.accounts.update_one(
            {'_id': ObjectId(account_id)},
            {'$pull': {'transactions': ObjectId(transaction_id)}}
        )    
            return {"message": f"Transaccion {transaction_id} eliminada"}
    except Exception as e:
        print(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)})
    
    
"""
    Crear objeto transacciones
    cursor(Transaction_db): Datos de la transaccion de base de datos
    wlopera
    @Jun 2024
    return  Datos de la transaccion de la cuenta
"""
def create_transaction(cursor):
    cursor["id"] = str(cursor["_id"])
    del cursor["_id"]   
    return Transaction(**cursor)
        
