from fastapi import HTTPException, status, Depends
from pydantic import EmailStr
# 이 줄이 성공적으로 실행되어야 합니다.
from app.utils.auth import get_password_hash, verify_password, create_access_token, decode_access_token
from typing import Dict, Any, Optional
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta

# 실제 데이터베이스(DB) 역할을 대체하는 임시 사용자 저장소
fake_users_db: Dict[EmailStr, Dict[str, Any]] = {} 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_user(email: EmailStr, password: str):
    """
    새로운 사용자를 생성하고 비밀번호를 해시하여 저장합니다.
    """
    if email in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 비밀번호 해시
    hashed_password = get_password_hash(password)
    # 임시 DB에 저장
    fake_users_db[email] = {"email": email, "hashed_password": hashed_password}
    
    return {"email": email, "message": "User created successfully"}

def authenticate_user(email: EmailStr, password: str) -> Optional[Dict[str, str]]:
    """
    사용자 이메일과 비밀번호를 검증하고, 성공 시 액세스 토큰 정보를 반환합니다.
    """
    user = fake_users_db.get(email)
    if not user:
        return None  # 사용자 없음
    
    # 비밀번호 검증
    if not verify_password(password, user["hashed_password"]):
        return None  # 비밀번호 불일치

    # 인증 성공: 토큰 생성
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    JWT 토큰을 검증하여 현재 로그인된 사용자 객체를 반환합니다.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 토큰 디코딩 및 검증
    payload = decode_access_token(token)
    
    if payload is None:
        raise credentials_exception

    # 디코딩된 이메일을 사용자 ID로 사용
    user_email = payload.get("email")
    if user_email is None:
        raise credentials_exception
    
    # 실제 DB에서 사용자를 찾아 반환 (현재는 임시 DB 사용)
    user = fake_users_db.get(user_email)
    if user is None:
        # 토큰은 유효했지만 사용자가 DB에 없음 (탈퇴 등)
        raise credentials_exception 
        
    return user