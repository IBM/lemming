from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from schemas import *

import os
import json


app = Flask(__name__)
CORS(app)

app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
def hello_world():
    return "<p>Lemming!</p>"


@app.route("/landmarks", methods=["POST"])
def landmarks() -> List[Landmark]:
    payload: PlanningTask = json.loads(request.get_data().decode("utf-8"))

    landmarks = []
    return jsonify(landmarks)

if __name__ == "__main__":
    app.run(debug=False, port=int(os.getenv("PORT", 1234)), host="0.0.0.0")
