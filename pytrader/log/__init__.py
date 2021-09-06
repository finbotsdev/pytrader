# encoding: utf-8

import config
from datetime import datetime
import os
import logging
import logging.config
import threading

class ThreadLogFilter(logging.Filter):
    """
    This filter only shows log entries for specified thread name
    """

    def __init__(self, thread_name, *args, **kwargs):
        logging.Filter.__init__(self, *args, **kwargs)
        self.thread_name = thread_name

    def filter(self, record):
        return record.threadName == self.thread_name

def config_root_logger():
    log_path = create_log_folder()
    log_file = f'{log_path}/logger.log'

    formatter = "%(asctime)-15s" \
                "| %(threadName)-11s" \
                "| %(levelname)-5s" \
                "| %(message)s"

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'root_formatter': {
                'format': formatter
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'root_formatter'
            },
            'log_file': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'filename': log_file,
                'formatter': 'root_formatter',
            }
        },
        'loggers': {
            '': {
                'handlers': [
                    'console',
                    'log_file',
                ],
                'level': 'DEBUG',
                'propagate': True
            }
        }
    })


def create_log_folder():
    path = os.path.join(
      config.FILES_PATH,
      log_date,
      log_time
    )
    os.makedirs(path, exist_ok=True)
    return path


def start_thread_logging():
    """
    Add a log handler to separate file for current thread
    """
    thread_name = threading.Thread.getName(threading.current_thread())
    log_path = create_log_folder(config.FILES_PATH)
    log_file = f'{log_path}/perThreadLogging-{thread_name}.log'
    log_handler = logging.FileHandler(log_file)

    log_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)-15s"
        "| %(threadName)-11s"
        "| %(levelname)-5s"
        "| %(message)s")
    log_handler.setFormatter(formatter)

    log_filter = ThreadLogFilter(thread_name)
    log_handler.addFilter(log_filter)

    logger = logging.getLogger()
    logger.addHandler(log_handler)

    return log_handler


def stop_thread_logging(log_handler):
    logging.getLogger().removeHandler(log_handler)
    log_handler.close()


log_date = datetime.now().strftime("%Y.%m.%d")
log_time = datetime.now().strftime("%H.%M.%S")

logger = logging
config_root_logger()
