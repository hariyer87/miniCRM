from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core.security import create_access_token, get_password_hash
from app.models import User
from app.schemas.user import Token, UserOut
from app.services.audit import log_action

router = APIRouter()


@router.post("/login", response_model=Token)
def login(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = deps.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        log_action(db, "LOGIN_FAILED", "user", None, None, f"username {form_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = create_access_token(user.id, user.role, timedelta(minutes=deps.settings.access_token_expire_minutes))
    log_action(db, "LOGIN_SUCCESS", "user", user.id, user.id, None)
    return Token(access_token=access_token, user=user)


@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(deps.get_current_user)):
    return current_user
