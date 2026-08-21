# responsibe for:
# Receive Mood, latitude, longigue
# call get_recommendations() and then Return JSON

# Imports
from services.recommendation_engine import get_recommendations
from services.gemini import analyze_user_request

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
    user_input = data.get("user_input")
    mood = data.get("mood")

    if not all([latitude, longitude]):
        return jsonify({"error": "Latitude and longitude are required"}), 400

    if not mood and not user_input:
            return jsonify({"error": "Either mood or user_input is required"}), 400

    # AI integration
    analysis = None

    if user_input:
         analysis = analyze_user_request(user_input)
         
    

    #Getting recommendations
    result = get_recommendations(latitude=latitude, longitude=longitude, user_mood=mood, analysis=analysis)

   

    return jsonify(result), 200
