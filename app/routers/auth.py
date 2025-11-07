from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserOut, Token
from app.crud.user import create_user, authenticate_user, create_access_token, get_current_user
from app.models.user import User, UserRole  # Импорт модели и enum для ролей

router = APIRouter(prefix="/auth", tags=["auth"])

# Кастомная схема для куки (для Swagger отображается как Bearer, но мы используем куки)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = create_user(db, user.dict())
    return created_user

@router.post("/login", response_model=Token)
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)  # Здесь username - это email
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value},  # Добавлена роль в токен
        expires_delta=access_token_expires
    )
    # Установка куки: HTTP-Only, Secure (в продакшене), SameSite=Strict
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,  # 30 минут
        expires=1800,
        secure=False,  # В dev - False, в prod - True
        samesite="strict"
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

# Dependency для извлечения токена из куки
def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if token.startswith("Bearer "):
        token = token.split("Bearer ")[1]
    return token

# Базовая зависимость для текущего пользователя
def get_current_user_from_cookie(db: Session = Depends(get_db), token: str = Depends(get_token_from_cookie)):
    return get_current_user(db, token)

# Зависимости для проверки ролей
def get_current_admin(current_user: User = Depends(get_current_user_from_cookie)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions: Admin required")
    return current_user

def get_current_hotel_manager(current_user: User = Depends(get_current_user_from_cookie)):
    if current_user.role != UserRole.HOTEL_MANAGER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions: Hotel Manager required")
    return current_user

# ... (Аналогично добавьте для других ролей, если нужно: CONTENT_MODERATOR, etc.)

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user_from_cookie)):
    return current_user

# Пример защищенного эндпоинта только для админа (список всех пользователей)
@router.get("/admin/users", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    users = db.query(User).all()
    return users