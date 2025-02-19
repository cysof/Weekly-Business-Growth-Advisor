from fastapi import APIRouter
from app.services import generate_insight

router = APIRouter(prefix="/insights", tags=["Insights"])

@router.get("/")
def get_weekly_insight():
    return generate_insight()
