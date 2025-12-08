from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# ----------------------------------------------------------------------
# 설정 (실제 프로젝트에서는 환경 변수로 관리해야 합니다.)
# ----------------------------------------------------------------------
SECRET_KEY = "YOUR_SUPER_SECRET_KEY_REPLACE_ME_NOW" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------------------------------------------------------------
# 1. 비밀번호 해시 함수
# ----------------------------------------------------------------------
def get_password_hash(password: str) -> str:
    """
    주어진 비밀번호 문자열의 해시 값을 반환합니다.
    """
    return pwd_context.hash(password)

# ----------------------------------------------------------------------
# 2. 비밀번호 검증 함수
# ----------------------------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    일반 비밀번호와 해시된 비밀번호를 비교하여 일치 여부를 반환합니다.
    """
    return pwd_context.verify(plain_password, hashed_password)

# ----------------------------------------------------------------------
# 3. 액세스 토큰 생성 함수
# ----------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    JWT 액세스 토큰을 생성합니다.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # 만료 시간을 기본 30분으로 설정
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # "sub" 필드는 토큰의 주체(Subject)로 사용되며, 여기서는 이메일이 들어갑니다.
    to_encode.update({"exp": expire})
    
    # JWT 인코딩
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ----------------------------------------------------------------------
# 4. 토큰 디코딩 및 검증 함수
# ----------------------------------------------------------------------
def decode_access_token(token: str):
    """
    JWT 액세스 토큰을 디코딩하고 검증합니다.
    """
    try:
        # JWT 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 이메일(sub) 필드 추출
        email: str = payload.get("sub")
        if email is None:
            return None # sub 필드가 없음
        return {"email": email}
    except JWTError:
        return None # 토큰 검증 실패 (만료, 변조 등)