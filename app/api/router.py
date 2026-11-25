from fastapi import APIRouter
from app.api.authentication import router as auth_router

router = APIRouter(prefix='/monitoring-api', tags=['Website Monitoring API'])

router.include_router(auth_router)


