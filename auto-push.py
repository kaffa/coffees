import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re
import subprocess
import shutil


class Watcher:
    path = sys.argv[1] if len(sys.argv) > 1 else os.getenv('USERPROFILE') + '\\Downloads'
    
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(3)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)

            if re.match(r"tiddlywiki \([\d+]*?\).html", event.src_path.split('\\').pop()):
                shutil.copyfile(event.src_path, 'index.html')
                subprocess.Popen(f'cmd /c "aio.cmd"', shell=True)


if __name__ == '__main__':
    w = Watcher()
    w.run()
