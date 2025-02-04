from fastapi import FastAPI
from tablemate_api.routes.auth_routes import router as auth_router
from tablemate_api.routes.protected_routes import router as protected_router

app = FastAPI()

# Include authentication and protected routes
app.include_router(auth_router)
app.include_router(protected_router)

@app.get("/")
def home():
    return {"message": "Welcome to TableMate API"}
