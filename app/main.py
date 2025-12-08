from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth

app = FastAPI(
    title="예약 시스템 API",
    description="레스토랑/병원 예약 시스템",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Reservation System API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}