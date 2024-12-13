import logging
import logging.handlers
import os
import sys
from urllib.parse import urlparse

from definitions import ROOT_DIR


class Logger:
    @staticmethod
    def create_logger(debug_filename, logger_name, enabled=False):
        """Creates a logger format for error logging
        :debug_filename: path and filename of the debug log
        :logger_name: name of the logger to create
        :enabled: enable to write the log to provided filename, otherwise uses a NullHandler
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s:%(name)s:%(funcName)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        if enabled and not os.path.isdir("logs"):
            os.makedirs("logs", exist_ok=True)

        if enabled:
            debug_log_handler = logging.handlers.RotatingFileHandler(
                f"logs/{debug_filename}", encoding="utf-8", mode="w"
            )
            debug_log_handler.setLevel(logging.DEBUG)
            debug_log_handler.setFormatter(formatter)
            logger.addHandler(debug_log_handler)
        else:
            logger.addHandler(logging.NullHandler())

        return logger


def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


def get_project_root():
    return ROOT_DIR


def get_file_index_path():
    if getattr(sys, "frozen", False):
        # The application is frozen (packaged)
        base_path = sys._MEIPASS
    else:
        base_path = get_project_root()

    file_index_path = os.path.join(base_path, "src", "file_index")
    return file_index_path


def validate_repo_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc


def print_all_indexes(directory):
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    items = os.listdir(directory)
    folders = [item for item in items if os.path.isdir(os.path.join(directory, item))]

    if folders:
        print("\nAll folders in 'src/file_index':")
        for folder in folders:
            print(f"- {folder}")
    else:
        print(f"No folders found in '{directory}'.")
