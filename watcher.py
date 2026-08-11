from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ai import analyze_image
from actions import rename_and_move
import time
import json


def get_watch_folder():
    try:
        with open("data/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        return config.get("watch_folder", "watched")

    except (FileNotFoundError, json.JSONDecodeError):
        return "watched"


def get_watch_folders():
    try:
        with open("data/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        return config.get("folders", ["Other"])

    except (FileNotFoundError, json.JSONDecodeError):
        return ["Other"]


observer = None


class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(".crdownload"):
            return

        folders = get_watch_folders()

        result = analyze_image(
            event.src_path,
            folders
        )

        if result:
            rename_and_move(event.src_path, result)


def start_watching():
    global observer

    if observer is not None:
        return

    observer = Observer()

    watch_folder = get_watch_folder()

    observer.schedule(
        Watcher(),
        watch_folder,
        recursive=False
    )

    observer.start()

    print(f"Watching folder: {watch_folder}")


def stop_watching():
    global observer

    if observer is None:
        return

    observer.stop()
    observer.join()

    observer = None

    print("Stopped watching.")


if __name__ == "__main__":
    start_watching()

    try:
        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:
        stop_watching()