import os
import shutil
import json
from datetime import datetime


def rename_and_move(file_path, result):
    filename = result["filename"]
    folder = result["folder"]

    extension = os.path.splitext(file_path)[1]

    destination_folder = os.path.join("watched", folder)

    os.makedirs(destination_folder, exist_ok=True)

    new_file = os.path.join(
        destination_folder,
        filename + extension
    )

    shutil.move(file_path, new_file)

    history_file = "data/history.json"

    with open(history_file, "r") as file:
        history = json.load(file)

    history.append({
        "old_name": os.path.basename(file_path),
        "new_name": filename + extension,
        "folder": folder,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)

    print(f"Moved to: {new_file}")