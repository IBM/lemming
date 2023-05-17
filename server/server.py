from flask import Flask, request, jsonify
from flask_cors import CORS
from schemas import PlanningTask, LemmingTask, Plan
from typing import Any, List

import os
import json
import requests
import networkx

from networkx.readwrite import json_graph

config = json.loads(open("config.json").read())
app = Flask(__name__)
CORS(app)

app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
def hello_world() -> Any:
    return "<p>Lemming!</p>"


@app.route("/file_upload", methods=["POST"])
def file_upload() -> Any:
    payload = request.get_data().decode("utf-8")
    return jsonify(payload)


@app.route("/import_domain", methods=["POST"])
def import_domain() -> Any:
    payload = json.loads(request.get_data().decode("utf-8"))
    domain_name: str = payload["name"]

    planning_task = PlanningTask(
        domain=open(f"./data/{domain_name}/domain.pddl").read(),
        problem=open(f"./data/{domain_name}/problem.pddl").read(),
    )

    try:
        plans = json.load(open(f"./data/{domain_name}/plans.json"))
        plans = [Plan(actions=item["actions"], cost=item["cost"]) for item in plans]

    except Exception as e:
        print(e)
        plans = []

    new_lemming_task = LemmingTask(planning_task=planning_task, plans=plans)
    return jsonify(new_lemming_task.dict())


@app.route("/get_landmarks", methods=["POST"])
def get_landmarks() -> Any:
    landmarks: Any = []
    return jsonify(landmarks)


@app.route("/get_plans", methods=["POST"])
def get_plans() -> Any:
    payload: Any = json.loads(request.get_data().decode("utf-8"))
    planning_task = PlanningTask(**payload)
    plans: List[Plan] = []

    if config.get("use_planner", True):
        server_url = config["planner_url"]
        endpoint = config["planner_endpoints"]["plans"]
        url = f"{server_url}/planners/{endpoint}"

        planner_payload = {
            "domain": planning_task.domain,
            "problem": planning_task.problem,
            "numplans": 5,
            "qualitybound": 1,
        }

        result = requests.post(
            url,
            json=planner_payload,
            timeout=config["TIMEOUT"],
            verify=False,
        )

        if result.status_code == 200:
            result = result.json()
            plans = result.get("plans", [])

    return jsonify(plans)


@app.route("/generate_select_view", methods=["POST"])
def generate_select_view() -> Any:
    # UNDER CONSTRUCTION #
    dot_graph = networkx.nx_pydot.read_dot("./data/example.dot")
    return json_graph.node_link_data(dot_graph)


@app.route("/generate_build_forward", methods=["POST"])
def generate_build_forward() -> Any:
    viz: Any = None
    return jsonify(viz)


@app.route("/generate_build_backward", methods=["POST"])
def generate_build_backward() -> Any:
    viz: Any = None
    return jsonify(viz)


@app.route("/generate_landmarks_view", methods=["POST"])
def generate_landmarks_view() -> Any:
    viz: Any = None
    return jsonify(viz)


@app.route("/new_selection", methods=["POST"])
def new_selection() -> Any:
    viz: Any = dict()
    return jsonify(viz)


if __name__ == "__main__":
    app.run(debug=False, port=int(os.getenv("PORT", 1234)), host="0.0.0.0")
