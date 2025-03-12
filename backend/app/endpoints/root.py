from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Welcome to Home Inventory Manager API!"}

@router.get("/api/health")
async def health_check():
    return {"status": "healthy"} 