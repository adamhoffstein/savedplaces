import json
import time
from typing import Tuple
from functools import lru_cache
from requests import Session, Request
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.services.utils import flatten, sort_by_key


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
            while pages < 2:
                time.sleep(5)
                results = self.get_request(
                    url,
                    {
                        "pagetoken": results.get("next_page_token"),
                        "key": self.key,
                    },
                )
                print([r.get("name") for r in results["results"]])
                pages += 1
                all_results.append(results["results"])
                if not results.get("next_page_token"):
                    break
        return flatten(all_results)


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


def nearby_mock(
    lat: float, lon: float, radius: int, type: str, rating: float, keyword: str
):
    formatted_keyword = keyword.lower().replace(" ", "_")
    try:
        with open(f"app/mock_data/response_{formatted_keyword}.json") as f:
            data = f.read()
        json.loads(data)
        return [
            d
            for d in sort_by_key(
                flatten(json.loads(data)), "user_ratings_total"
            )
            if d.get("rating") >= rating
        ]
    except Exception as e:
        print(e)
        return []
