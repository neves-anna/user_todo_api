from fastapi import FastAPI

from user_todo_api.routers import auth, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
