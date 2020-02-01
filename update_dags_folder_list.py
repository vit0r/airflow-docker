"""Update dags folders on task.json
"""

import sys
from json import dumps, load
from pathlib import Path

FROM_DIR = sys.argv[1]
VSCODE_TASK_PATH = Path(FROM_DIR, ".vscode", "tasks.json")


def write_new_task_json(str_json: str) -> None:
    """
    Write a new file task.json with plugins and dags folders
    :param str_json: task.json content as string
    :return: None
    """
    if str_json:
        tasks_file = VSCODE_TASK_PATH.open(mode="w+")
        tasks_file.truncate()
        tasks_file.write(str_json)
        tasks_file.close()


def update_input_options(
    folder_regex: str, input_id: str, element_name="default"
) -> None:
    """
    Update values for input / dags and plugins
    :param folder_regex: regex to find dags directories
    :param input_id: task.json input id
    :param element_name: elemente of input to receive all dags or plugins paths
    :return: None
    """
    print(f"find ... {folder_regex}")
    folders = list(map(str, Path.glob(Path.home(), folder_regex)))
    tasks_file = VSCODE_TASK_PATH.open(mode="r")
    tasks_json = load(tasks_file)
    tasks_file.close()
    str_json = None
    for inputv in tasks_json.get("inputs"):
        if inputv.get("id") == input_id:
            inputv[element_name] = folders if len(folders) > 1 else folders[0]
            str_json = dumps(tasks_json, indent=2)
    write_new_task_json(str_json)


if __name__ == "__main__":
    try:
        update_input_options("**/dags/", "dagsFolder", "options")
        update_input_options("**/airflow-plugins/", "pluginsFolder")
    except Exception as ex:
        sys.exit(1)
    finally:
        sys.exit(0)
