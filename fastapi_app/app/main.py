from fastapi import FastAPI
from fastapi_app.app.routes import users, posts

app = FastAPI()

# Подключение маршрутов
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI app!"}
