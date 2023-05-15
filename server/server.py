from flask import Flask, request, jsonify
from flask_cors import CORS
from schemas import *
from typing import List, Any

import os
import json

config = json.loads(open("config.json").read())
app = Flask(__name__)
CORS(app)

app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
def hello_world():
    return "<p>Lemming!</p>"


@app.route("/file_upload", methods=["POST"])
def file_upload():
    payload = request.get_data().decode("utf-8")
    return jsonify(payload)


@app.route("/import_domain", methods=["POST"])
def import_domain() -> LemmingTask:

    payload = json.loads(request.get_data().decode("utf-8"))
    domain_name: str = payload["name"]

    planning_task = PlanningTask(
      domain=open(f'./data/{domain_name}/domain.pddl').read(),
      problem=open(f'./data/{domain_name}/problem.pddl').read(),
    )

    try:
        plans = json.load(open(f'./data/{domain_name}/plans.json'))
        plans = [Plan(steps=item["plan"], cost=item["cost"]) for item in plans["plans"]]

    except Exception as e:
        print(e)
        plans = []

    new_lemming_task = LemmingTask(
      planning_task=planning_task,
      plans=plans
    )

    return jsonify(new_lemming_task.dict())


@app.route("/get_landmarks", methods=["POST"])
def get_landmarks(planning_task: PlanningTask) -> List[Landmark]:

    if not planning_task:
        planning_task = PlanningTask(json.loads(request.get_data().decode("utf-8")))

    # Call to service
    _ = planning_task

    landmarks = []
    return jsonify(landmarks)


@app.route("/get_plans", methods=["POST"])
def get_plans(planning_task: PlanningTask) -> List[Plan]:

    if not planning_task:
        planning_task = PlanningTask(json.loads(request.get_data().decode("utf-8")))

    # Call to service
    _ = planning_task

    plans = []
    return jsonify(plans)


@app.route("/generate_selection_view", methods=["POST"])
def generate_selection_view(lemming_task: LemmingTask, landmarks: List[Landmark]) -> Any:

    if not lemming_task or not landmarks:
        payload = json.loads(request.get_data().decode("utf-8"))

        lemming_task = LemmingTask(payload["lemming_task"])
        landmarks = [Landmark(item) for item in payload["landmarks"]]

    # Call to service
    _ = lemming_task, landmarks

    viz = dict()
    return jsonify(viz)


@app.route("/new_selection", methods=["POST"])
def new_selection(selections: List[Selection]) -> Any:

    if not selections:
        payload = json.loads(request.get_data().decode("utf-8"))
        selections = payload

    # Call to service
    _ = selections

    viz = dict()
    return jsonify(viz)


if __name__ == "__main__":
    app.run(debug=False, port=int(os.getenv("PORT", 1234)), host="0.0.0.0")
