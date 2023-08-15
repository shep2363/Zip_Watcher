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
    def process(self, event):
        if event.is_directory:
            return None
        
        print(f"Detected file event ({event.event_type}): {event.src_path}")
        
        if event.src_path.endswith('.zip'):
            # Adding a short delay might help ensure the .zip file is completely written before processing.
            time.sleep(3)
            try:
                self.unzip_file(event.src_path)
            except Exception as e:
                print(f"Failed to unzip {event.src_path}. Error: {e}")

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

    def on_moved(self, event):
        # For moved event, the destination path is more relevant
        event.src_path = event.dest_path
        self.process(event)

    def unzip_file(self, zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            unzip_dir = os.path.dirname(zip_path)
            zip_ref.extractall(unzip_dir)
            print(f"Extracted {zip_path} to {unzip_dir}")

if __name__ == "__main__":
    w = Watcher("C:\\Users\\fab.automation\\Downloads")
    w.run()
