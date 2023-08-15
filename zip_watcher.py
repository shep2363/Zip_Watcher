import os
import time
import zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    """
    This class sets up a watchdog observer to watch a directory for changes.
    """

    def __init__(self, directory_to_watch):
        """
        Initialize the watcher with the directory it should observe.
        """
        self.DIRECTORY_TO_WATCH = directory_to_watch
        self.observer = Observer()

    def run(self):
        """
        Start the observer and keep it running. It will trigger the handler for specified events.
        """
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        while True:
            time.sleep(5)

class Handler(FileSystemEventHandler):
    """
    This class defines the event handler that is triggered by the observer.
    """

    def process(self, event):
        """
        Process events caught by the watchdog. This method is primarily looking for 'created' events to detect new files.
        """
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # Check if the created file is a .zip file and unzip it if it is.
            if event.src_path.endswith('.zip'):
                self.unzip_file(event.src_path)

    def on_created(self, event):
        """
        Event handler for the 'created' event.
        """
        self.process(event)

    def unzip_file(self, zip_path):
        """
        Unzips the specified file into its current directory.
        """
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            unzip_dir = os.path.dirname(zip_path)
            zip_ref.extractall(unzip_dir)
            print(f"Extracted {zip_path} to {unzip_dir}")

if __name__ == "__main__":
    # Set up a watcher on the Downloads directory and start it.
    w = Watcher("C:\\Users\\fab.automation\\Downloads")
    w.run()
