from app import app, io
from dotenv import dotenv_values
import os
from time import sleep
from clear import clear
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

values = dotenv_values()


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, tracked_files):
        super().__init__()
        self.tracked_files = tracked_files

    def on_modified(self, event):
        """Triggered when something is modified."""
        if os.path.basename(event.src_path) == "version":

            print(
                f"Mudança detectada no arquivo {event.src_path}, reiniciando o servidor Flask..."
            )
            clear()
            restart_flask()


def start_flask():
    port = int(values.get("PORT", 5000))
    debug = values.get("DEBUG", "False").lower() in ("true", "1", "t", "y", "yes")

    io.run(app, "0.0.0.0", port=int(port), debug=debug, use_reloader=False)


def flask_Thread():
    flask_Thread = Thread(target=start_flask)
    flask_Thread.start()
    return flask_Thread


def restart_flask():
    global flask_server_Thread
    if flask_server_Thread.is_alive():
        clear()
        flask_server_Thread.terminate()
        flask_server_Thread.join(15)

    flask_server_Thread = flask_Thread()
    print("Servidor Flask reiniciado.")


def monitor_changes():

    root_path = os.path.join(os.getcwd())
    tracked_file = os.path.join(os.getcwd(), ".version")
    with open(tracked_file, "w") as f:
        f.write("LATEST")

    event_handler = ChangeHandler(tracked_file)
    observer = Observer()
    observer.schedule(event_handler, path=root_path, recursive=True)
    observer.start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    print("Iniciando monitoramento de mudanças e servidor Flask...")

    # Inicia o servidor Flask
    flask_server_Thread = flask_Thread()

    # Inicia o monitoramento das mudanças
    monitor_changes()
