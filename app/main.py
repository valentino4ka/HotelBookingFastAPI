from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.room import router as room_router
from app.routers.admin import router as admin_router
from app.routers.hotel_manager import router as manager_router
from app.routers.content_moderator import router as moderator_router
from app.routers.user import router as user_router
from app.routers.booking import router as booking_router


app = FastAPI(title="HotelBooking API")

app.include_router(auth_router, prefix="/api/v1")
app.include_router(room_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(manager_router, prefix="/manager")
app.include_router(moderator_router, prefix="/moderator")
app.include_router(user_router, prefix="/user")
app.include_router(booking_router, prefix="/api/v1")

@app.get("/")
def health():
    return {"status": "ok"}
