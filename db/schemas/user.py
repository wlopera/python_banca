# Esquema de la DB User
def user_schema(user, field) -> dict:
    return {
        field: str(user[field]),
        "login": user["login"],
        "password": user["password"],
        "enabled": user["enabled"],
        "type": user["type"]
}
       
def users_schema(users, field) -> list:
    return [user_schema(user, field) for user in users]
