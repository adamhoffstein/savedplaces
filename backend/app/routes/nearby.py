from fastapi import APIRouter
from app.services import places

router = APIRouter()


@router.get("/")
def get_nearby_places(
    lat: float, lon: float, radius: int, rating: float, keyword: str
):
    return places.nearby(
        lat=lat,
        lon=lon,
        radius=radius,
        type="restaurant",
        rating=rating,
        keyword=keyword,
    )


@router.get("/mock")
def get_mock_nearby_places(
    lat: float, lon: float, radius: int, rating: float, keyword: str
):
    return places.nearby_mock(
        lat=lat,
        lon=lon,
        radius=radius,
        type="restaurant",
        rating=rating,
        keyword=keyword,
    )
