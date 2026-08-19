# responsibe for:
# Receive Mood, latitude, longigue
# call get_recommendations() and then Return JSON

# Imports
from services.recommendation_engine import get_recommendations

from flask import Blueprint, request, jsonify

recommendation_bp = Blueprint("recommendation", __name__)


@recommendation_bp.route("/recommendations", methods=["POST", "OPTIONS"])
def recommendations():
    if request.method == 'OPTIONS':
        return '', 204

    # Getting data from frontend
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    mood = data.get("mood")

    if not all([latitude, longitude, mood]):
        return jsonify({"error": "Latitude, longitude, and mood are required"}), 400

    

    #Getting recommendations
    print("mood from frontend:", mood)
    result = get_recommendations(user_mood=mood, latitude=latitude, longitude=longitude)

    return jsonify(result), 200
