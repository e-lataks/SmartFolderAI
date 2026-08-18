import os
import shutil
import json
from datetime import datetime


def get_config():
    try:
        with open(
            "data/config.json",
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "watch_folder": "watched",
            "sort_into_folders": False
        }


def rename_and_move(file_path, result):
    filename = result["filename"]
    folder = result["folder"]

    config = get_config()

    watch_folder = config.get(
        "watch_folder",
        "watched"
    )

    sort_into_folders = config.get(
        "sort_into_folders",
        False
    )

    extension = os.path.splitext(file_path)[1]

    if sort_into_folders:
        destination_folder = os.path.join(
            watch_folder,
            folder
        )

        os.makedirs(
            destination_folder,
            exist_ok=True
        )

    else:
        destination_folder = watch_folder

    new_file = os.path.join(
        destination_folder,
        filename + extension
    )

    shutil.move(
        file_path,
        new_file
    )

    os.makedirs(
        "data",
        exist_ok=True
    )

    history_file = "data/history.json"

    try:
        with open(
            history_file,
            "r",
            encoding="utf-8"
        ) as file:
            history = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append({
        "old_name": os.path.basename(file_path),
        "new_name": filename + extension,
        "folder": folder,
        "watch_folder": watch_folder,
        "time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })

    with open(
        history_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            history,
            file,
            indent=4
        )

    print(f"Moved to: {new_file}")