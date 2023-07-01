from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple
from networkx import Graph
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    SelelctionInfo,
    PlanningTask,
    Plan,
    PlannerResponseModel,
    ChoiceInfo,
)
from helpers.planner_helper.planner_helper import get_dot_graph_str
from helpers.graph_helper.graph_helper import (
    convert_dot_str_to_networkx_graph,
    get_node_edge_name_plan_hash_list,
    get_graph_with_number_of_plans_label,
)


def get_first_achievers(landmarks: Optional[List[Landmark]]) -> List[List[str]]:
    if landmarks is None or len(landmarks) == 0:
        return []
    return list(map(lambda landmark: landmark.first_achievers, landmarks))


def split_plans_with_actions(
    action_names: List[str],
    plans: List[Plan],
    previous_selected_actions: Set[str],
) -> Tuple[Dict[str, List[int]], Dict[str, List[str]], int]:
    """
    returns a tuple of 1) a dictionary of first_achiever names and lists of plan indices
    and 2) the maximum number of plans with a first achiever
    """
    plan_sets: List[Set[str]] = list(map(lambda plan: set(plan.actions), plans))
    action_name_list_plan_idx: Dict[str, List[int]] = dict()
    action_name_list_plan_hash: Dict[str, List[str]] = dict()
    plan_hashes_for_action: Set[str] = set()

    for action_name in action_names:  # first achievers
        for plan_set_idx, plan_set in enumerate(plan_sets):
            if (
                action_name in plan_set
                and action_name not in previous_selected_actions
            ):
                if action_name not in action_name_list_plan_idx:
                    action_name_list_plan_idx[action_name] = list()
                    action_name_list_plan_hash[action_name] = list()
                action_name_list_plan_idx[action_name].append(plan_set_idx)
                action_name_list_plan_hash[action_name].append(
                    plans[plan_set_idx].plan_hash
                )
                plan_hashes_for_action.add(plans[plan_set_idx].plan_hash)
        if action_name in action_name_list_plan_idx and len(
            action_name_list_plan_idx[action_name]
        ) == len(
            plans
        ):  # remove an action, which cannot disambiguate plans
            action_name_list_plan_idx.pop(action_name, None)
            action_name_list_plan_hash.pop(action_name, None)

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
    return get_plans_filetered_by_selected_plan_hashes(selection_info, plans)


def get_plans_with_selection_infos(
    selection_infos: Optional[List[SelelctionInfo]],
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
        selected_plans = get_plans_filetered_by_selected_plan_hashes(
            selection_info, plans
        )
    return selected_plans


def get_split_by_actions(
    landmarks: List[Landmark],
    plans: List[Plan],
    selection_infos: List[SelelctionInfo],
) -> List[ChoiceInfo]:
    """
    return a list of landmark infos
    (1) a landmark, 2) the maximum number of plans including a first achiever,
    and 3) a dictionary of first achiever name and a list of plan indices)
    """
    previous_selected_actions = set(
        map(
            lambda selection_info: selection_info.selected_first_achiever,
            selection_infos,
        )
    )
    choice_infos: List[ChoiceInfo] = list()
    for landmark in landmarks:
        (
            action_name_plan_idx_list,
            action_name_plan_hash_list,
            num_plans_in_actions,
        ) = split_plans_with_actions(
            landmark.first_achievers, plans, previous_selected_actions
        )
        if (
            num_plans_in_actions > 0
        ):  # only consider landmarks shown in given plans
            choice_infos.append(
                ChoiceInfo(
                    landmark=landmark.copy(deep=True),
                    max_num_plans=num_plans_in_actions,
                    action_name_plan_idx_map=action_name_plan_idx_list,  # keys are first-achievers available fore the next choice
                    action_name_plan_hash_map=action_name_plan_hash_list,  # keys are first-achievers available fore the next choice
                    is_available_for_choice=num_plans_in_actions > 0,
                )
            )

    return sorted(
        choice_infos,
        key=lambda info: info.max_num_plans,
        reverse=False,
    )


def get_filtered_landmark_by_selected_plans(
    landmarks: List[Landmark], selected_plans: List[Plan]
) -> List[Landmark]:
    plan_hash_actions_dict: Dict[str, Set[str]] = dict()
    for plan in selected_plans:
        plan_hash_actions_dict[plan.plan_hash] = set(plan.actions)
    filtered_landmarks: List[Landmark] = list()
    for landmark in landmarks:
        counter_valid_first_achievers = 0
        for first_achiever in landmark.first_achievers:
            for actions_set in plan_hash_actions_dict.values():
                if first_achiever in actions_set:
                    counter_valid_first_achievers += 1
                    break
        if counter_valid_first_achievers >= 2:
            filtered_landmarks.append(landmark.copy(deep=True))
    return filtered_landmarks


def get_plan_disambiguator_output_filtered_by_selection_infos(
    selection_infos: List[SelelctionInfo],
    landmarks: List[Landmark],
    domain: str,
    problem: str,
    plans: List[Plan],
) -> Tuple[
    List[Plan],
    List[ChoiceInfo],
    Graph,
    str,
    Dict[str, List[str]],
    Dict[Tuple[str, str], List[str]],
]:
    """
    returns 1) filtered plans, 2) filtered and sorted landmarks,
    landmarks information, 3) a graph, 4) a graph in dot string
    """
    selected_plans = get_plans_with_selection_infos(selection_infos, plans)
    dot_str = get_dot_graph_str(
        PlanningTask(domain=domain, problem=problem),
        planning_results=PlannerResponseModel.get_planning_results(
            PlannerResponseModel(plans=selected_plans)
        ),
    )
    g = convert_dot_str_to_networkx_graph(dot_str)
    (
        node_plan_hashes_dict,
        edge_plan_hash_dict,
    ) = get_node_edge_name_plan_hash_list(g, selected_plans, True)
    g = get_graph_with_number_of_plans_label(g, node_plan_hashes_dict)
    choices = get_split_by_actions(landmarks, selected_plans, selection_infos)
    return (
        selected_plans,
        choices,
        g,
        dot_str,
        node_plan_hashes_dict,
        edge_plan_hash_dict,
    )


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
        nodes_with_multiple_out_edges=[node_with_multiple_edges],
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


def append_landmarks_not_avialable_for_choice(
    landmarks: List[Landmark], choice_infos: List[ChoiceInfo]
) -> List[ChoiceInfo]:
    choice_infos_with_not_available_landmarks: List[ChoiceInfo] = list(
        map(lambda choice_info: choice_info.copy(deep=True), choice_infos)
    )
    facts_set: Set[Tuple] = set()
    for choice_info in choice_infos:
        if choice_info.landmark is not None:
            facts_set.add(tuple(choice_info.landmark.facts))

    for landmark in landmarks:
        if (
            tuple(landmark.facts) not in facts_set
            and len(landmark.first_achievers) >= 2
        ):
            choice_infos_with_not_available_landmarks.append(
                ChoiceInfo(
                    landmark=landmark.copy(deep=True),
                    is_available_for_choice=False,
                )
            )

    return choice_infos_with_not_available_landmarks
