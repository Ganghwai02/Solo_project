from sqlalchemy import create_engine
from app.database import Base
from app.models import User, Restaurant, Reservation

# 직접 DATABASE_URL 설정
DATABASE_URL = "postgresql://reservation_user:reservation_pass@localhost:5432/reservation_db"

# 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)

# 모든 테이블 생성
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")