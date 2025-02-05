from fastapi import FastAPI
from tablemate_api.routes.auth_routes import router as auth_router
from tablemate_api.routes.protected_routes import router as protected_router
from tablemate_api.routes.restaurants import router as restaurants_router
from tablemate_api.routes.profile_info import router as profile_info
from tablemate_api.middleware import add_cors

app = FastAPI()
add_cors(app)
# Include authentication and protected routes
app.include_router(profile_info)
app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(restaurants_router)
@app.get("/")
def home():
    return {"message": "Welcome to TableMate API"}
