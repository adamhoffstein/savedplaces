from fastapi import APIRouter
from app.services import places

router = APIRouter()


@router.get("/")
def get_nearby_places(
    lat: float, lon: float, radius: int, type: str, rating: float, keyword: str
):
    return places.nearby(
        lat=lat,
        lon=lon,
        radius=radius,
        type=type,
        rating=rating,
        keyword=keyword,
    )
