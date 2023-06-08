import hashlib
from typing import Any, List


def get_hash(data: Any) -> str:
    dhash = hashlib.md5()
    dhash.update(data)
    return dhash.hexdigest()


def get_list_hash(lst: List[str]) -> str:
    return get_hash(bytearray(str(tuple(lst)), "utf-8")) if len(lst) > 0 else ""
