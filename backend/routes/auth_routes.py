
from flask import Flask, request, jsonify
from database.connection import getDatabase
from database.user_queries import createAccount, login
from flask import Blueprint

auth_bp = Blueprint("auth", __name__)
@auth_bp.route("/signup", methods=["POST"])
def signupMethod():
    

    #Getting info from frontend 
    data = request.get_json()
    print("Received data:", data["username"], data["email"], data["password"])

    # Estabish a connection to the MySQL database and return that connection
    db = getDatabase()
    if db is None:
        return jsonify({"message": "Database connection failed."}), 500

    #Calling createAccount function
    _, success = createAccount(db, data["username"], data["email"], data["password"])
    db.close()

    # Output
    if success:
        return jsonify({"message": "Account created"}), 201
    else:
        return jsonify ({"message": "Account creation failed."}), 400


@auth_bp.route("/login", methods=["POST"])
def loginMethod():
    

    #Getting data from the frontend
    data = request.get_json()

    #Getting database and check for success
    db = getDatabase()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    # Calling Login
    _, user = login(db, data["email"], data["password"])

    db.close()

    # Output depending on success
    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    else:
        return jsonify({"message": "Invalid login credentials"}), 401
    