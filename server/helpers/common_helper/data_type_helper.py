from typing import Any, List, Set


def merge_sets(sets: List[Set[Any]]) -> Set[Any]:
    merged_set: Set[Any] = set()
    for s in sets:
        for item in s:
            merged_set.add(item)
    return merged_set
