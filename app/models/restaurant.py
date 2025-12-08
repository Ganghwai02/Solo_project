from sqlalchemy import Column, Integer, String, Text, Time, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    # 영업 시간
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)

    # 예약 설정
    slot_duration = Column(Integer, default=60) # 예약 시간 단위 (분)
    max_capacity = Column(Integer, default=10) # 시간대별 최대 예약 수

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계 설정
    reservations = relationship("Reservation", back_populates="restaurant")