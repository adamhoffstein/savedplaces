from ast import keyword
from functools import lru_cache
from typing import Tuple
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from requests import Session, Request
import time


class GooglePlacesClient:
    base_url = "https://maps.googleapis.com/maps/api/place"

    def __init__(self, key: str) -> None:
        self.key = key
        self.next_page_token = None
        self.session = Session()

    def get_request(self, url, params):
        preparedRequest = Request("GET", url, params=params).prepare()
        print(f"Sending GET request to {preparedRequest.url}")
        return self.session.send(preparedRequest).json()

    def places_nearby(
        self,
        location: Tuple[float, float],
        radius: int,
        type: str,
        keyword: str,
    ):
        original_params = {
            "location": f"{location[0]},{location[1]}",
            "type": type,
            "keyword": keyword,
            "radius": radius,
            "key": self.key,
        }
        url = f"{self.base_url}/nearbysearch/json?"
        all_results = []
        results = self.get_request(url, original_params)
        all_results.append(results["results"])
        pages = 0
        if results.get("next_page_token"):
            while pages < 2 and results.get("next_page_token"):
                results = self.get_request(
                    url,
                    {
                        "pagetoken": results.get("next_page_token"),
                        "key": self.key,
                    },
                )
                pages += 1
                all_results.append(results["results"])
                time.sleep(1)
        return all_results


@lru_cache
def get_gmaps_places_client() -> AppSettings:
    settings = get_app_settings()
    return GooglePlacesClient(key=settings.google_places_key)


def nearby(
    lat: float, lon: float, radius: int, type: str, rating: float, keyword: str
):
    results = get_gmaps_places_client().places_nearby(
        location=(lat, lon), radius=radius, type=type, keyword=keyword
    )
    return results
