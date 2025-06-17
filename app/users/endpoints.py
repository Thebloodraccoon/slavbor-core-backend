from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.users.schemas import UserCreate, UserResponse, UserUpdate
from app.users.service import UserService
from app.settings import settings

router = APIRouter(prefix="/users", tags=["Users"])


# ── DI‑фабрика сервисов ──────────────────────────────────────────────────────
def _svc(db: Session = Depends(settings.get_db)):
    return UserService(db)


# ── CRUD‑роуты ───────────────────────────────────────────────────────────────
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(settings.get_db)):
    try:
        return svc.create_user(payload)
    except ValueError as err:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(err))


@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(settings.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
):
    return db.list_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, svc: UserService = Depends(_svc)):
    user = svc.get_user(user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate,  db: Session = Depends(settings.get_db)):
    try:
        return db.update_user(user_id, payload)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    except ValueError as err:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(err))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int,  db: Session = Depends(settings.get_db)):
    try:
        db.delete_user(user_id)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
