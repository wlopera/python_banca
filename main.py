from fastapi import FastAPI
from routers import users_db

app = FastAPI()

# Routers
app.include_router(users_db.router)
