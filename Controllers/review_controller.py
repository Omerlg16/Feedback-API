import os
import secrets
from functools import wraps

from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS
from Services.review_service import create_review, get_stats

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"))
CORS(app, resources={r"^/api/reviews$": {"origins": [
    "https://omerlg16.github.io",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]}})


def requires_auth(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        expected_user = os.environ.get("DASHBOARD_USER")
        expected_password = os.environ.get("DASHBOARD_PASSWORD")
        auth = request.authorization

        if not (expected_user and expected_password and auth):
            return _auth_required()
        if not (secrets.compare_digest(auth.username or "", expected_user)
                and secrets.compare_digest(auth.password or "", expected_password)):
            return _auth_required()

        return view(*args, **kwargs)
    return wrapper


def _auth_required():
    return Response(
        "Authentification requise",
        401,
        {"WWW-Authenticate": 'Basic realm="Dashboard"'}
    )


@app.route("/")
def home():
    return jsonify({"status": "ok"}), 200


@app.route("/api/reviews", methods=["POST"])
def create_review_route():
    payload = request.get_json(silent=True) or {}
    _, erreur = create_review(payload)

    if erreur:
        return jsonify({"error": erreur}), 400

    return jsonify({"message": "Avis enregistré"}), 201


@app.route("/api/reviews/stats", methods=["GET"])
@requires_auth
def stats_route():
    return jsonify(get_stats()), 200


@app.route("/dashboard")
@requires_auth
def dashboard_route():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
