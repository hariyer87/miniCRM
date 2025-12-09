from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.core.security import get_password_hash
from app.models import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.audit import log_action

router = APIRouter(dependencies=[Depends(deps.require_admin)])


@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(deps.get_db)):
    return db.query(User).all()


@router.post("", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.require_admin)):
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(
        username=user_in.username,
        full_name=user_in.full_name,
        role=user_in.role,
        is_active=user_in.is_active,
        password_hash=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    log_action(db, "CREATE_USER", "user", user.id, current_user.id, None)
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(deps.get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.require_admin)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user_in.dict(exclude_unset=True).items():
        if field == "password" and value:
            setattr(user, "password_hash", get_password_hash(value))
        else:
            setattr(user, field, value)
    db.commit()
    db.refresh(user)
    log_action(db, "UPDATE_USER", "user", user.id, current_user.id, None)
    return user


@router.patch("/{user_id}/deactivate", response_model=UserOut)
def deactivate_user(user_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.require_admin)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    db.refresh(user)
    log_action(db, "DEACTIVATE_USER", "user", user.id, current_user.id, None)
    return user
