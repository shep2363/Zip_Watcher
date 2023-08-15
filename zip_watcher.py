import os
import time
import zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    def __init__(self, directory_to_watch):
        self.DIRECTORY_TO_WATCH = directory_to_watch
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        print(f"Watching directory: {self.DIRECTORY_TO_WATCH}")
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    extraction_count = 0

    def on_moved(self, event):
        if event.is_directory:
            return None

        file_path = event.dest_path
        print(f"Detected file event ({event.event_type}): {file_path}")

        if file_path.endswith('.zip'):
            time.sleep(1)  # A short delay to ensure the .zip file is fully written.
            try:
                self.unzip_file(file_path)
            except Exception as e:
                print(f"Failed to unzip {file_path}. Error: {e}")

    def unzip_file(self, zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            Handler.extraction_count += 1
            base_unzip_dir = os.path.dirname(zip_path)
            specific_unzip_dir = os.path.join(base_unzip_dir, f"Extracted_{Handler.extraction_count}")
            os.makedirs(specific_unzip_dir, exist_ok=True)

            zip_ref.extractall(specific_unzip_dir)
            print(f"Extracted {zip_path} to {specific_unzip_dir}")

if __name__ == "__main__":
    w = Watcher("C:\\Users\\fab.automation\\Downloads")
    w.run()
