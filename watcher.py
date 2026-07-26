from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg")

class FolderWatcher(FileSystemEventHandler):
    def on_created(self, event):

        if event.is_directory:
            return

        if event.src_path.endswith(".crdownload"):
            return

        if not event.src_path.lower().endswith(IMAGE_EXTENSIONS):
            return

        print(f"New image detected: {event.src_path}")

if __name__ == "__main__":
    path = "watched"

    observer = Observer()
    observer.schedule(FolderWatcher(), path, recursive=False)
    observer.start()

    print(f"Watching folder: {path}")

    try:
        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    9