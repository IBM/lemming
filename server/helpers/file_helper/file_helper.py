import json
from os import listdir
from os.path import join, abspath, isfile, isdir
from pathlib import Path
from typing import List
from pydantic import BaseModel


def create_folders_if_not_exist(path_str: str):
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
    return [abspath(join(root_path, name)) for name in listdir(root_path) if isdir(join(root_path, name))]


def get_file_paths_in_folder(root_path: str) -> List[str]:
    return [abspath(join(root_path, name)) for name in listdir(root_path) if isfile(join(root_path, name))]
