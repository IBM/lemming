from typing import List, Optional
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    Plan,
    SelelctionInfo,
    PlanDisambiguatorOutput,
)
from helpers.graph_helper.graph_helper import get_dict_from_graph
from helpers.common_helper.exception_handler import planner_exception_handler
from helpers.plan_disambiguator_helper.plan_disambiguator_helper import (
    get_plan_disambiguator_output_filtered_by_selection_infos,
    get_choice_info_multiple_edges_without_landmark,
)
from helpers.graph_helper.graph_helper import (
    get_first_node_with_multiple_out_edges_forward,
)


@planner_exception_handler
def get_selection_flow_output(
    selected_landmarks: Optional[List[SelelctionInfo]],
    landmarks: List[Landmark],
    domain: str,
    problem: str,
    plans: List[Plan],
) -> PlanDisambiguatorOutput:
    (
        selected_plans,
        landmark_infos,
        g,
        _,
    ) = get_plan_disambiguator_output_filtered_by_selection_infos(
        selected_landmarks, landmarks, domain, problem, plans
    )
    networkx_graph = get_dict_from_graph(g)
    if (
        len(selected_plans) > 1 and len(landmark_infos) == 0
    ):  # no landmarks for disambiguating plans
        (
            node_with_multiple_out_edges,
            _,
            _,
            edges_traversed,
        ) = get_first_node_with_multiple_out_edges_forward(g, dict())

        return PlanDisambiguatorOutput(
            plans=selected_plans,
            choice_infos=[
                get_choice_info_multiple_edges_without_landmark(
                    node_with_multiple_out_edges=node_with_multiple_out_edges,
                    edges_traversed=edges_traversed,
                    plans=selected_plans,
                )
            ],
            networkx_graph=networkx_graph,
        )

    return PlanDisambiguatorOutput(
        plans=selected_plans,
        choice_infos=landmark_infos,
        networkx_graph=networkx_graph,
    )
