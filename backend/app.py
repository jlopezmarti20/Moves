
# Post /locationmood -> Post /recommendations
# responsibe for:
# Receive Mood, latitude, longigue
# call get_recommendations() and then Return JSON

# Imports
from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.recommendation_routes import recommendation_bp
from routes.bookmark_routes import bookmark_bp



app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(bookmark_bp)


@app.route("/")
def home():
    return {"message": "Moves backend is running!"}



if __name__ == "__main__":
    app.run(debug=True, port=5555)