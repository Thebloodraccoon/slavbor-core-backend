from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.settings import settings
from app.users.schemas import UserCreate, UserResponse, UserUpdate
from app.users.services import UserService

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_all_users(
    page: int = Query(0, ge=0, description="Page number (0-indexed)"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    db: Session = Depends(settings.get_db),
):
    """Get all users with pagination."""
    return UserService(db).get_all_users(page=page, size=size)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(settings.get_db)):
    """Get user by ID."""
    return UserService(db).get_user_by_id(user_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(settings.get_db)):
    """Create a new user."""
    return UserService(db).create_user(user_data)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, user_data: UserUpdate, db: Session = Depends(settings.get_db)
):
    """Update user by ID."""
    return UserService(db).update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(settings.get_db)):
    """Delete user by ID."""
    UserService(db).delete_user(user_id)
    return None
