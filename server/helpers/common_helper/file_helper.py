from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    from _typeshed import SupportsRead

import json

from fastapi import File, UploadFile


def read_str_from_upload_file(file: UploadFile = File(...)) -> Optional[str]:
    try:
        contents: str = file.file.read().decode("utf-8")
        return contents
    except Exception as e:
        print(e)
    finally:
        file.file.close()

    return None


def read_str_from_file(path: str) -> str:
    with open(path, "r") as f:
        content = f.read()
        return content


def write_str_on_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def convert_json_str_to_dict(ip: SupportsRead[Union[str, bytes]]) -> Any:
    return json.load(ip)
