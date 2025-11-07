from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.room import router as room_router


app = FastAPI(title="HotelBooking API")

app.include_router(auth_router, prefix="/api/v1")
app.include_router(room_router, prefix="/api/v1")

@app.get("/")
def health():
    return {"status": "ok"}
