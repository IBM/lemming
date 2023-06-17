from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple

from helpers.graph_helper.graph_helper import (
    convert_dot_str_to_networkx_graph,
    get_graph_with_number_of_plans_label,
    get_node_name_plan_hash_list,
)
from helpers.planner_helper.planner_helper import get_dot_graph_str
from helpers.planner_helper.planner_helper_data_types import (
    ChoiceInfo,
    Landmark,
    Plan,
    PlannerResponseModel,
    PlanningTask,
    SelelctionInfo,
)
from networkx import Graph


def get_filtered_out_selection_infos_by_selection_infos(
    landmarks: List[Landmark], selection_infos: List[SelelctionInfo]
) -> List[Landmark]:
    selected_first_achievers = (
        set(
            map(
                lambda selection_info: selection_info.selected_first_achiever[
                    :
                ],
                selection_infos,
            )
        )
        if selection_infos is not None
        else set()
    )
    selected_facts = (
        set(
            map(
                lambda selection_info: tuple(selection_info.facts),
                selection_infos,
            )
        )
        if selection_infos is not None
        else set()
    )
    filtered_landmarks: List[Landmark] = list()
    for landmark in landmarks:
        if tuple(landmark.facts) in selected_facts:
            continue
        filtered_first_achievers: Set[str] = set()
        for first_achiever in landmark.first_achievers:
            if first_achiever not in selected_first_achievers:
                filtered_first_achievers.add(first_achiever[:])
        if len(filtered_first_achievers) > 1:
            filtered_landmark = landmark.copy(deep=True)
            filtered_landmark.first_achievers = list(filtered_first_achievers)
            filtered_landmarks.append(filtered_landmark)
    return filtered_landmarks


def get_first_achievers(landmarks: Optional[List[Landmark]]) -> List[List[str]]:
    if landmarks is None or len(landmarks) == 0:
        return []
    return list(map(lambda landmark: landmark.first_achievers, landmarks))


def get_filtered_in_landmark_by_selection_info(
    selection_info: SelelctionInfo, landmarks: List[Landmark]
) -> List[Landmark]:
    return list(
        map(
            lambda filtered_landmark: filtered_landmark.copy(deep=True),
            filter(
                lambda landmark: landmark.facts == selection_info.facts,
                landmarks,
            ),
        )
    )


def get_filtered_out_landmark_by_selection_info(
    selection_info: SelelctionInfo, landmarks: List[Landmark]
) -> List[Landmark]:
    return list(
        map(
            lambda filtered_landmark: filtered_landmark.copy(deep=True),
            filter(
                lambda landmark: landmark.facts != selection_info.facts,
                landmarks,
            ),
        )
    )


def split_plans_with_actions(
    action_names: List[str], plans: List[Plan]
) -> Tuple[Dict[str, List[int]], Dict[str, List[str]], int]:
    """
    returns a tuple of 1) a dictionary of first_achiever names and lists of plan indices
    and 2) the maximum number of plans with a first achiever
    """
    plan_sets: List[Set[str]] = list(map(lambda plan: set(plan.actions), plans))
    action_name_list_plan_idx: Dict[str, List[int]] = dict()
    action_name_list_plan_hash: Dict[str, List[str]] = dict()
    for plan_set_idx, plan_set in enumerate(plan_sets):
        for action_name in action_names:
            if action_name in plan_set:
                if action_name not in action_name_list_plan_idx:
                    action_name_list_plan_idx[action_name] = list()
                    action_name_list_plan_hash[action_name] = list()
                action_name_list_plan_idx[action_name].append(plan_set_idx)
                action_name_list_plan_hash[action_name].append(
                    plans[plan_set_idx].plan_hash
                )
    num_remaining_plans = (
        0
        if len(action_name_list_plan_idx) == 0
        else max(
            [
                len(plan_indices)
                for plan_indices in action_name_list_plan_idx.values()
            ]
        )
    )
    return (
        action_name_list_plan_idx,
        action_name_list_plan_hash,
        num_remaining_plans,
    )


def get_plans_filetered_by_selected_plan_hashes(
    selection_info: SelelctionInfo, plans: List[Plan]
) -> List[Plan]:
    if (
        selection_info.selected_plan_hashes is None
        or len(selection_info.selected_plan_hashes) == 0
    ):
        return list(map(lambda plan: plan.copy(deep=True), plans))

    plan_hashes_to_select: Set[str] = set(selection_info.selected_plan_hashes)
    return list(
        filter(lambda plan: plan.plan_hash in plan_hashes_to_select, plans)
    )


def get_plans_with_selection_info(
    selection_info: SelelctionInfo, landmarks: List[Landmark], plans: List[Plan]
) -> List[Plan]:
    """
    returns plans filtered by a selected landmark
    """
    filtered_plans = get_plans_filetered_by_selected_plan_hashes(
        selection_info, plans
    )

    if len(filtered_plans) < len(plans):
        return filtered_plans

    selected_landmarks = get_filtered_in_landmark_by_selection_info(
        selection_info, landmarks
    )
    action_name_list_plan_idx, _, _ = split_plans_with_actions(
        selected_landmarks[0].first_achievers, plans
    )

    return [
        plans[idx].copy(deep=True)
        for idx in action_name_list_plan_idx[
            selection_info.selected_first_achiever
        ]
    ]


def get_plans_with_selection_infos(
    selection_infos: Optional[List[SelelctionInfo]],
    landmarks: List[Landmark],
    plans: List[Plan],
) -> List[Plan]:
    """
    returns plans filtered by selected landmarks
    """
    plans_before_filtering = list(map(lambda plan: plan.copy(deep=True), plans))

    if selection_infos is None or len(selection_infos) == 0:
        return plans_before_filtering

    selected_plans: List[Plan] = plans_before_filtering
    for selection_info in selection_infos:
        selected_plans = get_plans_with_selection_info(
            selection_info, landmarks, selected_plans
        )
    return selected_plans


def get_split_by_actions(
    landmarks: List[Landmark], plans: List[Plan]
) -> List[ChoiceInfo]:
    """
    return a list of landmark infos
    (1) a landmark, 2) the maximum number of plans including a first achiever,
    and 3) a dictionary of first achiever name and a list of plan indices)
    """
    first_achievers_max_num_plans_dict: List[ChoiceInfo] = list()
    for landmark in landmarks:
        (
            action_name_plan_idx_list,
            action_name_plan_hash_list,
            max_num_plans_with_first_achiever,
        ) = split_plans_with_actions(landmark.first_achievers, plans)
        if (
            max_num_plans_with_first_achiever > 0
        ):  # only consider landmarks shown in given plans
            first_achievers_max_num_plans_dict.append(
                ChoiceInfo(
                    landmark=landmark.copy(deep=True),
                    max_num_plans=max_num_plans_with_first_achiever,
                    action_name_plan_idx_map=action_name_plan_idx_list,
                    action_name_plan_hash_map=action_name_plan_hash_list,
                )
            )

    return sorted(
        first_achievers_max_num_plans_dict,
        key=lambda info: info.max_num_plans,
        reverse=False,
    )


def get_plan_disambiguator_output_filtered_by_selection_infos(
    selection_infos: List[SelelctionInfo],
    landmarks: List[Landmark],
    domain: str,
    problem: str,
    plans: List[Plan],
) -> Tuple[List[Plan], List[ChoiceInfo], Graph, str, Dict[str, List[str]]]:
    """
    returns 1) filtered plans, 2) filtered and sorted landmarks,
    landmarks information, 3) a graph, 4) a graph in dot string
    """
    selected_plans = get_plans_with_selection_infos(
        selection_infos, landmarks, plans
    )
    filtered_landmarks = get_filtered_out_selection_infos_by_selection_infos(
        landmarks, selection_infos
    )
    choice_infos = get_split_by_actions(filtered_landmarks, selected_plans)
    dot_str = get_dot_graph_str(
        PlanningTask(domain=domain, problem=problem),
        planning_results=PlannerResponseModel.get_planning_results(
            PlannerResponseModel(plans=selected_plans)
        ),
    )
    g = convert_dot_str_to_networkx_graph(dot_str)
    node_plan_hashes_dict = get_node_name_plan_hash_list(
        g, selected_plans, True
    )
    g = get_graph_with_number_of_plans_label(g, node_plan_hashes_dict)

    return selected_plans, choice_infos, g, dot_str, node_plan_hashes_dict


def get_merged_first_achievers_dict(
    choice_infos: List[ChoiceInfo],
) -> Dict[Any, List[Any]]:
    """
    return a dictionary of first achiever names (key) and plan indices
    """
    merged_dict: Dict[Any, List[Any]] = dict()
    for landmark_info in choice_infos:
        for k, v in landmark_info.action_name_plan_idx_map.items():
            merged_dict[k] = deepcopy(v)
    return merged_dict


def filter_in_choice_info_by_first_achiever(
    selection_infos: List[ChoiceInfo], first_achiever: Any
) -> List[ChoiceInfo]:
    for selection_info in selection_infos:
        if first_achiever in selection_info.action_name_plan_idx_map:
            return [selection_info.copy(deep=True)]
    return []


def get_plan_idx_edge_dict(
    edges_traversed: List[Any], plans: List[Plan], is_forward: bool
) -> Dict[int, Any]:
    len_edges_traversed = (
        len(edges_traversed) if is_forward else -(len(edges_traversed) + 1)
    )
    plan_idx_edge_dict: Dict[int, Any] = dict()
    for plan_idx, plan in enumerate(plans):
        plan_idx_edge_dict[plan_idx] = plan.actions[len_edges_traversed]
    return plan_idx_edge_dict


def get_edge_label_plan_hashes_dict(
    edges_traversed: List[Any], plans: List[Plan], is_forward: bool
) -> Dict[str, List[str]]:
    plan_idx_edges_dict = get_plan_idx_edge_dict(
        edges_traversed, plans, is_forward
    )
    edge_label_plan_hash_dict: Dict[str, List[str]] = dict()

    for plan_idx, edge_label in plan_idx_edges_dict.items():
        if edge_label not in edge_label_plan_hash_dict:
            edge_label_plan_hash_dict[edge_label] = list()
        edge_label_plan_hash_dict[edge_label].append(
            plans[plan_idx].plan_hash[:]
        )

    return edge_label_plan_hash_dict


def get_choice_info_multiple_edges_without_landmark(
    node_with_multiple_edges: str,
    edges_traversed: List[Any],
    plans: List[Plan],
    is_forward: bool,
) -> ChoiceInfo:
    return ChoiceInfo(
        node_with_multiple_out_edges=node_with_multiple_edges,
        action_name_plan_hash_map=get_edge_label_plan_hashes_dict(
            edges_traversed, plans, is_forward
        ),
    )


def get_first_achiever_out_edge_dict(
    edges_traversed: List[Any],
    plans: List[Plan],
    turn_choice_info: ChoiceInfo,
    is_forward: bool,
) -> Dict[Any, List[Any]]:
    # TODO: TEST THIS
    """
    returns a dictionary of first achiever and out edges
    """
    first_achiever_edge_dict: Dict[Any, List[Any]] = dict()
    plan_idx_edges_dict = get_plan_idx_edge_dict(
        edges_traversed, plans, is_forward
    )
    for (
        first_achiever,
        list_plan_idx,
    ) in turn_choice_info.action_name_plan_idx_map.items():
        first_achiever_edge_dict[first_achiever] = list(
            set(
                map(
                    lambda plan_idx: plan_idx_edges_dict[plan_idx],
                    list_plan_idx,
                )
            )
        )
    return first_achiever_edge_dict


def append_landmarks_not_available_for_choice(
    landmarks: List[Landmark], choice_infos: List[ChoiceInfo]
) -> List[ChoiceInfo]:
    choice_infos_with_not_available_landmarks: List[ChoiceInfo] = list(
        map(lambda choice_info: choice_info.copy(deep=True), choice_infos)
    )
    facts_set: Set[Tuple[Any, ...]] = set()
    for choice_info in choice_infos:
        if choice_info.landmark is not None:
            facts_set.add(tuple(choice_info.landmark.facts))

    for landmark in landmarks:
        if tuple(landmark.facts) not in facts_set:
            choice_infos_with_not_available_landmarks.append(
                ChoiceInfo(
                    landmark=landmark.copy(deep=True),
                    is_available_for_choice=False,
                )
            )

    return choice_infos_with_not_available_landmarks
