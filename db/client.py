from pymongo import MongoClient

# Conexion a DB local (localhost)
db_client = MongoClient().local

# Conexion a DB remota en Mongo Atlas - Agregar la url en unas vaqriables de ambientes para ocultar las claves
# Mi esquema lo llamo test
# db_client = MongoClient("mongodb+srv://admin:admin@cluster0.gioxlj8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test