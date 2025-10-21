from fastapi import APIRouter, Depends

from app.dependencies import verify_api_key

router = APIRouter(
    prefix="/activities",
    tags=["activities"],
    dependencies=[Depends(verify_api_key)],
)
