from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.owner_routes import router as owner_router
from app.routes.vehicle_routes import router as vehicle_router
from app.routes.driver_routes import router as driver_router
from app.routes.trip_routes import router as trip_router

app = FastAPI(title="Radiotaxis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RUTAS
app.include_router(vehicle_router)
app.include_router(owner_router)
app.include_router(driver_router)
app.include_router(trip_router)

@app.get("/")
def home():
    return {
        "message": "Backend funcionando"
    }