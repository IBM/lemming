from collections import defaultdict
import random
import sys
from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple
from networkx import Graph

from planners.drivers.planner_driver_datatype import PlanningResult
from helpers.planner_helper.planner_helper_data_types import (
    ChoiceInfo,
    Landmark,
    Plan,
    PlanningTask,
    SelectionInfo,
    SelectionPriority,
)
from helpers.planner_helper.planner_helper import get_dot_graph_str
from helpers.graph_helper.graph_helper import (
    convert_dot_str_to_networkx_graph,
    get_node_edge_name_plan_hash_list,
    get_graph_with_number_of_plans_label,
    get_node_distance_from_terminal_node,
    get_edge_label,
)


def get_min_dist_between_nodes_from_terminal_node_by_node(
    nodes: List[str],
    node_dist_from_terminal_state: Dict[str, int],
) -> int:
    min_dist = sys.maxsize
    for node in nodes:
        if node in node_dist_from_terminal_state:
            if node_dist_from_terminal_state[node] < min_dist:
                min_dist = node_dist_from_terminal_state[node]
    return min_dist


def get_min_dist_between_nodes_from_terminal_node(
    edge_labels: List[str],
    edge_label_nodes_dict: Dict[str, List[str]],
    node_dist_from_terminal_state: Dict[str, int],
) -> int:
    min_dist = sys.maxsize
    for edge_label in edge_labels:
        if edge_label in edge_label_nodes_dict:
            for node in edge_label_nodes_dict[edge_label]:
                if node in node_dist_from_terminal_state:
                    if node_dist_from_terminal_state[node] < min_dist:
                        min_dist = node_dist_from_terminal_state[node]
    return min_dist


def set_nodes_with_multiple_edges(
    choice_infos_input: List[ChoiceInfo],
    edge_label_nodes: Dict[str, List[str]],
) -> List[ChoiceInfo]:
    choice_infos = list(
        map(
            lambda choice_info: choice_info.model_copy(deep=True),
            choice_infos_input,
        )
    )
    for i in range(len(choice_infos)):
        nodes_with_target_edges: Set[str] = set()
        for edge_label in choice_infos[i].action_name_plan_hash_map.keys():
            if edge_label in edge_label_nodes:
                nodes_with_target_edges.update(edge_label_nodes[edge_label])
        choice_infos[i].nodes_with_multiple_out_edges = list(
            nodes_with_target_edges
        )
    return choice_infos


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
    returns a tuple of 1) a dictionary of first_achiever names and lists of plan
    indices and 2) the maximum number of plans with a first achiever
    """
    plan_sets: List[Set[str]] = list(
        map(lambda plan: set(plan.actions), plans))
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

                if plans[plan_set_idx].plan_hash is not None:
                    plan_hashes_for_action.add(
                        plans[plan_set_idx].plan_hash  # type: ignore
                    )
                    action_name_list_plan_hash[action_name].append(
                        plans[plan_set_idx].plan_hash  # type: ignore
                    )

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
    selection_info: SelectionInfo, plans: List[Plan]
) -> List[Plan]:
    if (
        selection_info.selected_plan_hashes is None
        or len(selection_info.selected_plan_hashes) == 0
    ):
        return list(map(lambda plan: plan.model_copy(deep=True), plans))

    plan_hashes_to_select: Set[str] = set(selection_info.selected_plan_hashes)
    return list(
        filter(lambda plan: plan.plan_hash in plan_hashes_to_select, plans)
    )


def get_plans_with_selection_info(
    selection_info: SelectionInfo, plans: List[Plan]
) -> List[Plan]:
    """
    returns plans filtered by a selected landmark
    """
    return get_plans_filetered_by_selected_plan_hashes(selection_info, plans)


def get_plans_with_selection_infos(
    selection_infos: Optional[List[SelectionInfo]],
    plans: List[Plan],
) -> List[Plan]:
    """
    returns plans filtered by selected landmarks
    """
    if len(plans) == 0:
        return []
    plans_before_filtering = list(
        map(lambda plan: plan.model_copy(deep=True), plans)
    )

    if selection_infos is None or len(selection_infos) == 0:
        return plans_before_filtering

    filtered_plan_hashes: Set[str] = set(
        selection_infos[0].selected_plan_hashes)
    for i in range(len(selection_infos) - 1):
        if len(selection_infos[i+1].selected_plan_hashes) > 0:
            filtered_plan_hashes = filtered_plan_hashes.intersection(
                set(selection_infos[i+1].selected_plan_hashes))
    filtered_plans = list(filter(
        lambda plan: plan.plan_hash in filtered_plan_hashes, plans_before_filtering))
    return filtered_plans if len(filtered_plans) > 0 else plans_before_filtering


def get_split_by_actions(
    landmarks: List[Landmark],
    plans: List[Plan],
    selection_infos: List[SelectionInfo],
) -> List[ChoiceInfo]:
    """
    return a list of landmark infos
    1) a landmark, 2) the maximum number of plans including a first achiever,
    and 3) a dictionary of first achiever name and a list of plan indices
    """
    previous_selected_actions = set(
        item.selected_first_achiever
        for item in selection_infos
        if item.selected_first_achiever
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
            len(action_name_plan_hash_list) > 0
        ):  # only consider landmarks shown in given plans
            choice_infos.append(
                ChoiceInfo(
                    landmark=landmark.model_copy(deep=True),
                    max_num_plans=num_plans_in_actions,
                    # keys are first-achievers available for the next choice
                    action_name_plan_idx_map=action_name_plan_idx_list,
                    # keys are first-achievers available for the next choice
                    action_name_plan_hash_map=action_name_plan_hash_list,
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
        if plan.plan_hash is not None:
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
            filtered_landmarks.append(landmark.model_copy(deep=True))
    return filtered_landmarks


def get_plan_disambiguator_output_filtered_by_selection_infos(
    selection_infos: List[SelectionInfo],
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
    Dict[str, List[str]],
    Dict[str, int],
    Dict[str, int],
]:
    """
    returns 1) filtered plans, 2) filtered and sorted landmarks,
    landmarks information, 3) a graph, 4) a graph in dot string
    """
    selected_plans = get_plans_with_selection_infos(selection_infos, plans)
    dot_str = get_dot_graph_str(
        planning_task=PlanningTask(domain=domain, problem=problem),
        planning_results=PlanningResult(plans=selected_plans),
    )
    g = convert_dot_str_to_networkx_graph(dot_str)
    node_dist_from_initial_state = get_node_distance_from_terminal_node(
        g, True)
    node_dist_from_end_state = get_node_distance_from_terminal_node(g, False)
    (
        node_plan_hashes_dict,
        edge_plan_hash_dict,
        edge_label_nodes_dict,
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
        edge_label_nodes_dict,
        node_dist_from_initial_state,
        node_dist_from_end_state,
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
            return [selection_info.model_copy(deep=True)]
    return []


def get_plan_idx_edge_dict(
    edges_traversed: List[Any], plans: List[Plan], is_forward: bool
) -> Dict[int, Any]:
    len_edges_traversed = (
        len(edges_traversed) if is_forward else -(len(edges_traversed) + 1)
    )
    plan_idx_edge_dict: Dict[int, Any] = dict()
    for plan_idx, plan in enumerate(plans):
        if (is_forward and len_edges_traversed < len(plan.actions)) or abs(len_edges_traversed) <= len(plan.actions):
            plan_idx_edge_dict[plan_idx] = plan.actions[len_edges_traversed]
    return plan_idx_edge_dict


def get_edge_label_plan_hashes_dict(
    edges_traversed: List[Any], plans: List[Plan], is_forward: bool
) -> Dict[str, List[str]]:
    plan_idx_edges_dict = get_plan_idx_edge_dict(
        edges_traversed, plans, is_forward
    )
    edge_label_plan_hash_dict: Dict[str, List[str]] = defaultdict(list)
    for plan_idx, edge_label in plan_idx_edges_dict.items():
        if plans[plan_idx].plan_hash:
            edge_label_plan_hash_dict[edge_label].append(
                plans[plan_idx].plan_hash  # type: ignore
            )

    return edge_label_plan_hash_dict


def get_plan_hashes_with_edges(edge_labels: List[str], plans: List[Plan]) -> Dict[str, List[str]]:
    action_name_plan_hashes_dict: Dict[str, List[str]] = defaultdict(list)
    for plan in plans:
        actions = set(plan.actions)
        for edge in edge_labels:
            if edge in actions:
                action_name_plan_hashes_dict[edge].append(plan.plan_hash)
    return action_name_plan_hashes_dict


def get_choice_info_multiple_edges_without_landmark(
    g: Graph,
    node_with_multiple_edges: str,
    node_plan_hashes_dict: Dict[str, List[str]],
    edges: List[Tuple[str, str]],
    edges_traversed: List[Any],
    plans: List[Plan],
    is_forward: bool,
) -> ChoiceInfo:
    plan_hashes_from_node = set(
        node_plan_hashes_dict[node_with_multiple_edges])
    filtered_plans = list(
        filter(lambda plan: plan.plan_hash in plan_hashes_from_node, plans))
    action_name_plan_hashes_dict = get_plan_hashes_with_edges(
        edge_labels=list(map(lambda edge: get_edge_label(g, edge), edges)), plans=filtered_plans)
    # action_name_plan_hash_map=get_edge_label_plan_hashes_dict(
    #             edges_traversed, plans, is_forward
    #         )
    return ChoiceInfo(
        nodes_with_multiple_out_edges=[node_with_multiple_edges],
        action_name_plan_hash_map=action_name_plan_hashes_dict,
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
        map(lambda cf: cf.model_copy(deep=True), choice_infos)
    )
    facts_set: Set[Tuple[Any, ...]] = set()
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
                    landmark=landmark.model_copy(deep=True),
                    is_available_for_choice=False,
                )
            )

    return choice_infos_with_not_available_landmarks


def get_total_num_plans(choice_info: ChoiceInfo) -> int:
    return sum(
        [len(plans) for plans in choice_info.action_name_plan_hash_map.values()]
    )


def sort_choice_info_by_distance_to_terminal_nodes(
    choice_infos_input: List[ChoiceInfo],
    node_dist_from_terminal_node: Dict[str, int],
) -> List[ChoiceInfo]:
    choice_infos = list(
        map(
            lambda choice_info: choice_info.model_copy(deep=True),
            choice_infos_input,
        )
    )
    choice_infos.sort(
        key=lambda cf: get_min_dist_between_nodes_from_terminal_node_by_node(
            list(cf.nodes_with_multiple_out_edges),
            node_dist_from_terminal_node,
        )
    )

    return choice_infos


def set_distance_to_terminal_nodes(
    choice_info_input: ChoiceInfo,
    node_dist_from_initial_state: Dict[str, int],
    node_dist_from_end_state: Dict[str, int],
) -> ChoiceInfo:
    choice_info: ChoiceInfo = choice_info_input.model_copy(deep=True)
    choice_info.distance_to_init = (
        get_min_dist_between_nodes_from_terminal_node_by_node(
            choice_info.nodes_with_multiple_out_edges,
            node_dist_from_initial_state,
        )
    )
    choice_info.distance_to_end = (
        get_min_dist_between_nodes_from_terminal_node_by_node(
            choice_info.nodes_with_multiple_out_edges,
            node_dist_from_end_state,
        )
    )
    return choice_info


def process_selection_priority(
    choice_infos_input: List[ChoiceInfo],
    selection_priority: Optional[str],
    edge_label_nodes_dict: Dict[str, List[str]],
    node_dist_from_initial_state: Dict[str, int],
    node_dist_from_end_state: Dict[str, int],
) -> List[ChoiceInfo]:
    choice_infos = list(
        map(
            lambda choice_info: choice_info.model_copy(deep=True),
            choice_infos_input,
        )
    )

    if (
        selection_priority is None
        or selection_priority == SelectionPriority.MAX_PLANS.value
        or selection_priority == SelectionPriority.MIN_PLANS.value
    ):
        choice_infos.sort(
            key=lambda choice_info: get_total_num_plans(choice_info),
            reverse=(selection_priority == SelectionPriority.MIN_PLANS.value),
        )
    elif selection_priority == SelectionPriority.RANDOM.value:
        random.shuffle(choice_infos)
    elif selection_priority == SelectionPriority.INIT_FORWARD.value:
        choice_infos.sort(
            key=lambda cf: get_min_dist_between_nodes_from_terminal_node(
                list(cf.action_name_plan_hash_map.keys()),
                edge_label_nodes_dict,
                node_dist_from_initial_state,
            )
        )
    elif selection_priority == SelectionPriority.GOAL_BACKWARD.value:
        choice_infos.sort(
            key=lambda cf: get_min_dist_between_nodes_from_terminal_node(
                list(cf.action_name_plan_hash_map.keys()),
                edge_label_nodes_dict,
                node_dist_from_end_state,
            )
        )

    return choice_infos
