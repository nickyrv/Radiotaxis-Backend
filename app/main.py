from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.owner_routes import router as owner_router
from app.routes.vehicle_routes import router as vehicle_router
from app.routes.driver_routes import router as driver_router
from app.routes.trip_routes import router as trip_router
from app.routes.shift_routes import router as shift_router
from app.routes.alert_routes import router as alert_router
from app.routes.payment_routes import router as payment_router
from app.routes.incident_routes import router as incident_router
from app.routes.auth_routes import router as auth_router
from fastapi.staticfiles import StaticFiles
from app.routes.vehicle_history_routes import router as vehicle_history_router

app = FastAPI(title="Radiotaxis API")
app.mount("/static", StaticFiles(directory="static"), name="static")

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
app.include_router(shift_router)
app.include_router(alert_router)
app.include_router(payment_router)
app.include_router(incident_router)
app.include_router(auth_router)
app.include_router(vehicle_history_router)

@app.get("/")
def home():
    return {
        "message": "Backend funcionando"
    }