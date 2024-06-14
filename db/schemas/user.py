def user_db_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "login": user["login"],
        "password": user["password"],
        "enabled": user["enabled"]    
    }
    
def users_db_schema(users) -> list:
    return [user_db_schema(user) for user in users]

def user_schema(user) -> dict:
    return {
        "login": user["login"],
        "enabled": user["enabled"]    
    }