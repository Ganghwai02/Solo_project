from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.services.auth import create_user, authenticate_user, get_current_user
from typing import Dict, Any

# Pydantic 스키마 정의
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: EmailStr
    
# APIRouter 인스턴스 생성
router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/register", response_model=User)
def register_user(user_data: UserCreate):
    """
    새로운 사용자 등록
    """
    # 서비스 계층 호출
    create_user(user_data.email, user_data.password)
    return {"email": user_data.email}

@router.post("/token", response_model=Token)
def login_for_access_token(user_data: UserCreate):
    """
    사용자 로그인 및 액세스 토큰 발급
    """
    # 서비스 계층 호출하여 인증
    auth_result = authenticate_user(user_data.email, user_data.password)
    
    if not auth_result:
        # 인증 실패 시 401 UNAUTHORIZED 반환
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_result

@router.get("/me", response_model=User)
async def read_users_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    현재 인증된 사용자 정보 가져오기 (토큰 필요)
    """
    return User(email=current_user["email"])