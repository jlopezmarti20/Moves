
import os
from services.google_places import get_city_from_coordinates , fetch_similar_google_places, haversine_distance, get_city_from_address
from config import mood_type_map
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")


# this file answer the question: Given a mood and a location, what places should I recommend?

def get_recommendations(latitude: float, longitude: float, user_mood: str = None, analysis: dict = None, rating_threshold: float=3.0) -> dict:

    city = get_city_from_coordinates(latitude, longitude)

    

    
    if analysis:
        
        mood_types = analysis["place_types"]
    else:
        
        mood_types = mood_type_map.get(user_mood.lower())

    

    all_businesses = []
    for place_type in mood_types:
        all_businesses += fetch_similar_google_places(city, place_type)

    

    # filtered to only business with rating of 3.0  or more
    filtered_businesses = []
    for business in all_businesses:
        rating = business.get("rating", 0)

        if rating >= rating_threshold:
            filtered_businesses.append(business)

    
   

    nearby_businesses = []
    for business in filtered_businesses:

        business_lat = business.get("geometry", {}).get("location", {}).get("lat")
        business_lon = business.get("geometry", {}).get("location", {}).get("lng")

        # skip if business don't have coordinates
        if business_lat is None or business_lon is None:
            continue

        distance_miles = haversine_distance(latitude, longitude, business_lat, business_lon) * 0.621371

        if distance_miles <= 30:
            nearby_businesses.append({"business": business, "distance": round(distance_miles, 2)})


    
    seen_place_ids = set()
    unique_businesses = []

    # removing duplicates businesses 
    for item in nearby_businesses:
        business = item["business"]

        place_id = business.get("place_id")

        if place_id in seen_place_ids:
            continue

        seen_place_ids.add(place_id)
        unique_businesses.append(item)


    unique_businesses.sort(key=lambda item: item["distance"])

    top_businesses = unique_businesses[:20]

    recommendations = []
    

    for item in top_businesses:
        business = item["business"]
        distance = item["distance"]

        photo_url = None

        if "photos" in business and business["photos"]:
            photo_name = business["photos"][0].get("name")

            if photo_name:
                photo_url = (
                    f"https://places.googleapis.com/v1/{photo_name}/media"
                    f"?maxWidthPx=400"
                    f"&key={GOOGLE_PLACES_API_KEY}"
                )

        # Format the response returned to the frontend
        
        recommendations.append({
            "place_id":business.get("place_id"),
            "name": business.get("name"),
            "rating": business.get("rating"),
            "address": business.get("formatted_address"),
            "categories": ", ".join(business.get("types", [])),
            "distance_miles": distance,
            "image": photo_url,
            "city": get_city_from_address(
                business.get("formatted_address", "")
            )
        })
    

    return {"recommendations": recommendations}

