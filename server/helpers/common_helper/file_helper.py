from __future__ import annotations
import json
from fastapi import File, UploadFile
from os import listdir, path
from os.path import join, abspath, isfile, isdir
from pathlib import Path
from typing import List
from pydantic import BaseModel
from typing import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    from _typeshed import SupportsRead


def create_folders_if_not_exist(path_str: str) -> None:
    path = Path(path_str)
    if not path.exists():
        path.mkdir(parents=True)


def create_file(file_path: Path, str_to_write: str = "") -> None:
    with open(file_path, "w") as f:
        f.write(str_to_write)


def create_file_from_base_model(file_path: Path, model: BaseModel) -> None:
    create_file(file_path=file_path, str_to_write=model.model_dump_json())


def get_model_from_file(file_path: Path, model: BaseModel) -> BaseModel:
    with open(file_path, "r") as f:
        tmp_dict = json.load(f)
    return model.model_validate(tmp_dict)


def append_string_to_file(file_path: Path, str_to_add: str) -> None:
    with open(file_path, "a") as f:
        f.write(str_to_add)


def get_subfolder_paths_in_folder(root_path: str) -> List[str]:
    return [
        abspath(join(root_path, name))
        for name in listdir(root_path)
        if isdir(join(root_path, name))
    ]


def get_file_paths_in_folder(root_path: str) -> List[str]:
    return [
        abspath(join(root_path, name))
        for name in listdir(root_path)
        if isfile(join(root_path, name))
    ]


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


def write_file_with_model_path(
    file_name: str, file_path: Path, file_extension: str, model: BaseModel
) -> Path:
    file_path = Path(path.join(file_path, file_name + "." + file_extension))
    create_file_from_base_model(file_path, model)
    return file_path
