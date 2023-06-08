from typing import Callable, Any


def planner_exception_handler(function: Callable[[Any], Any]) -> Any:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            result = function(*args, **kwargs)
            return result
        except Exception as e:
            print(e)
            return None

    return wrapper
