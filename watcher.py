from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ai import analyze_image
from actions import rename_and_move
import time


class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(".crdownload"):
            return

        result = analyze_image(event.src_path)

        if result:
            rename_and_move(event.src_path, result)


if __name__ == "__main__":
    path = "watched"

    observer = Observer()
    observer.schedule(Watcher(), path, recursive=False)
    observer.start()

    print(f"Watching folder: {path}")

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()