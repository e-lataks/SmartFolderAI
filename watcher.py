from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ai import analyze_image
from actions import rename_and_move
import time

WATCH_FOLDER = "watched"
observer = None

class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(".crdownload"):
            return

        result = analyze_image(event.src_path)

        if result:
            rename_and_move(event.src_path, result)


def start_watching():
    global observer

    if observer is not None:
        return

    observer = Observer()
    observer.schedule(Watcher(), WATCH_FOLDER, recursive=False)
    observer.start()

    print(f"Watching folder: {WATCH_FOLDER}")


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