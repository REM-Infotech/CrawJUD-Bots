# Criar loggers personalizados
import os
import logging
from logging.config import DictConfigurator

info_logger = None
warning_logger = None
error_logger = None


def loggerConfig() -> None:

    path_logs = os.path.join(os.getcwd(), "app", "logs")
    os.makedirs(path_logs, exist_ok=True)

    config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                # "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                "format": "[%(asctime)s] %(levelname)s in %(funcName)s: %(message)s",
            },
            "detailed": {
                # "format": "[%(asctime)s] %(levelname)s %(name)s in %(module)s: %(message)s",
                "format": "[%(asctime)s] %(levelname)s in %(funcName)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "app/logs/flask_app.log",
                "formatter": "detailed",
                "level": "DEBUG",
            },
            "wsgi": {  # Handler que usa wsgi_errors_stream para logs de erro WSGI
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
                "level": "INFO",
            },
            "socketio_file": {
                "class": "logging.FileHandler",
                "filename": "app/logs/socketio.log",
                "formatter": "detailed",
                "level": "DEBUG",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "file", "wsgi"],
        },
        "loggers": {
            "flask.app": {
                "level": "DEBUG",
                "handlers": ["console", "file", "wsgi"],
                "propagate": False,
            },
            "werkzeug": {
                "level": "DEBUG",
                "handlers": ["wsgi", "console"],
                "propagate": False,
            },
            "socketio": {  # Logger específico para flask_socketio
                "level": "DEBUG",
                "handlers": ["socketio_file", "wsgi"],
                "propagate": False,
            },
        },
    }

    DictConfigurator(config).configure()

    global info_logger
    info_logger = logging.getLogger("info_logger")

    global warning_logger
    warning_logger = logging.getLogger("warning_logger")

    global error_logger
    error_logger = logging.getLogger("error_logger")

    # # Teste de log para verificar se a configuração está funcionando
    # info_logger.info("This is an info message.")
    # warning_logger.warning("This is a warning message.")
    # error_logger.error("This is an error message.")
