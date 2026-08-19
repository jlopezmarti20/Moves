from flask import Blueprint, request, jsonify

from database.connection import getDatabase

from database.user_queries import saveBookmark, getBookmarks, removeBookmark

bookmark_bp = Blueprint("bookmark", __name__)


@bookmark_bp.route("/bookmark", methods=["POST"])
def saveBookmarkMethod():

    data = request.get_json()

    db = getDatabase()

    if db is None:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    place = {
        "place_id": data["place_id"],
        "name": data["name"],
        "address": data["address"],
        "rating": data["rating"],
        "image": data["image"],
        "categories": data["categories"],
        "distance_miles": data["distance_miles"]
    }

    _, success = saveBookmark(db, data["user_id"], place)

    db.close()

    if success:
        return jsonify({"message":"bookmark saved."}), 201

    return jsonify({"message":"Bookmark already exists."}), 400


@bookmark_bp.route("/bookmarks/<int:user_id>", methods=["GET"])
def getBookmarksMethod(user_id):

    db = getDatabase()

    if db is None:
        return jsonify({"message": "Database connection failed."}), 500

    
    _, bookmarks = getBookmarks(db, user_id)

    db.close()

    return jsonify({"bookmarks": bookmarks}), 200


@bookmark_bp.route("/bookmark/<place_id>/<int:user_id>", methods=["DELETE"])
def removeBookmarkMethod(place_id, user_id):

    db = getDatabase()
    
    if db is None:
        return jsonify({"message": "Database connection failed."}), 500

    removeBookmark(db, user_id, place_id)

    db.close()

    return jsonify({"message":"Bookmark removed"}), 200
    