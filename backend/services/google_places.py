import os
from dotenv import load_dotenv
import requests
from math import radians, cos, sin, asin, sqrt

load_dotenv()

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")



def get_city_from_coordinates(latitude: float, longitude: float) -> str:
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{latitude}, {longitude}",
        "key": GOOGLE_PLACES_API_KEY,
    }

    response = requests.get(url, params=params)
    results = response.json().get("results", [])
    if not results:
        return ""

    for component in results[0].get("address_components", []):
        if "locality" in component.get("types", []):
            return component.get("long_name")
    return ""

def get_city_from_address(address: str) -> str:
    parts = address.split(",")

    if len(parts) >= 3:
        return parts[-3].strip()

    return ""
    

def fetch_google_business(name: str, city: str):

    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": (
            "places.displayName,"
            "places.formattedAddress,"
            "places.location,"
            "places.rating,"
            "places.types,"
            "places.photos,"
            "places.id"
        )
    }

    body = {
        "textQuery": f"{name} {city}"
    }

    response = requests.post(url, headers=headers, json=body)

    places = response.json().get("places", [])

    if not places:
        return None

    place = places[0]

    return {
        "name": place.get("displayName", {}).get("text"),
        "formatted_address": place.get("formattedAddress"),
        "rating": place.get("rating", 0),
        "types": place.get("types", []),
        "place_id": place.get("id"),
        "geometry": {
            "location": {
                "lat": place.get("location", {}).get("latitude"),
                "lng": place.get("location", {}).get("longitude")
            }
        },
        "photos": place.get("photos", [])
    }


    

def fetch_similar_google_places(city: str, category_keywords: str):

    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": (
            "places.displayName,"
            "places.formattedAddress,"
            "places.location,"
            "places.rating,"
            "places.types,"
            "places.photos,"
            "places.id"
        )
    }

    body = {
        "textQuery": f"{category_keywords} in {city}"
    }

    

    response = requests.post(url, headers=headers, json=body)

   

    places = response.json().get("places", [])

    businesses = []

    for place in places:

        businesses.append({
            "name": place.get("displayName", {}).get("text"),
            "formatted_address": place.get("formattedAddress"),
            "rating": place.get("rating", 0),
            "types": place.get("types", []),
            "place_id": place.get("id"),
            "geometry": {
                "location": {
                    "lat": place.get("location", {}).get("latitude"),
                    "lng": place.get("location", {}).get("longitude")
                }
            },
            "photos": place.get("photos", [])
        })

    

    return businesses
    
# calculate longitude and lattitude
def haversine_distance(lat1, lon1, lat2, lon2):
  R = 6371  # Radius of the Earth in kilometer
  lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
  dlat = lat2 - lat1
  dlon = lon2 - lon1
  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  return R * 2 * asin(sqrt(a))
    



