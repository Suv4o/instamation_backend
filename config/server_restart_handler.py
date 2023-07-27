import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from waitress import serve
from config import SERVER_HOST, SERVER_PORT, Logger

console = Logger("app").get()


class ServerRestartHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == "modified":
            print("Restarting server...")
            os.execl(sys.executable, sys.executable, *sys.argv)


def run_server(app):
    event_handler = ServerRestartHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()
    try:
        console.info("Starting server...")
        serve(app, host=SERVER_HOST, port=SERVER_PORT)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
