import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from waitress import serve
from config.environments import PYTHON_ENV, SERVER_HOST, SERVER_PORT
from config.logging import Logger
from utils.enums import PythonEnv

console = Logger("app").get()


class ServerRestartHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif os.path.basename(event.src_path) == "requirements.txt":
            return None
        elif event.event_type == "modified":
            console.info("Restarting server...")
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


# This function is used to generate requirements.txt
# It is called from app.py only when the app is running in local environment
def generate_requirements():
    if PYTHON_ENV == PythonEnv.LOCAL.value:
        script_path = "_generate_requirements.sh"
        os.system(f"bash {script_path}")
        console.info("Requirements generated.")
