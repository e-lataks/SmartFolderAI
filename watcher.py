from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ai import analyze_image
from actions import rename_and_move
import time
import json
import os


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

        file_path = event.src_path
        extension = os.path.splitext(file_path)[1].lower()

        ignored_extensions = {
            ".tmp",
            ".crdownload",
            ".part",
            ".download"
        }

        if extension in ignored_extensions:
            return

        supported_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".gif"
        }

        if extension not in supported_extensions:
            return

        print(f"New image: {file_path}")

        folders = get_watch_folders()

        try:
            result = analyze_image(
                file_path,
                folders
            )

        except Exception as e:
            print(f"AI error: {e}")
            return

        if not result:
            print("AI did not return a result.")
            return

        try:
            rename_and_move(
                file_path,
                result
            )

        except Exception as e:
            print(f"File processing error: {e}")


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