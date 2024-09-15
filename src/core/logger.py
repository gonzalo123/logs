import hashlib
import logging
import sys
import json
from logging.handlers import TimedRotatingFileHandler
import time
from pathlib import Path

DEFAULT_FROM = 'appbeat'

LOG_RECORD_ATTRIBUTES = {
    'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
    'funcName', 'levelname', 'levelno', 'lineno', 'message', 'module',
    'msecs', 'msg', 'name', 'pathname', 'process', 'processName',
    'relativeCreated', 'stack_info', 'thread', 'threadName',
}

class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename: Path, app, when='M', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        self.filename = filename
        self.app = app
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)

    def rotation_filename(self, default_name):
        current_time = time.strftime("%Y-%m-%d_%H_%M")
        path = self.filename.resolve().parent
        return f"{path}/{self.app}.{current_time}.log.json"

class JsonFormatter(logging.Formatter):
    def __init__(self, app, process, *args, **kwargs):
        self.app = app
        self.process = process
        super().__init__(*args, **kwargs)

    def format(self, record):
        log_record = {
            'ts': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'message': record.getMessage(),
            'process': self.process,
            'app': self.app,
            'extra': {k: v for k, v in record.__dict__.items() if k not in LOG_RECORD_ATTRIBUTES}
        }
        md5_hash = hashlib.md5(json.dumps(log_record, sort_keys=True).encode()).hexdigest()
        log_record['hash'] = md5_hash
        return json.dumps(log_record)


def setup_logging(env, app, log_path, process='main', log_level='INFO'):
    if env == 'local':
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s] %(message)s',
            level=log_level,
            datefmt='%d/%m/%Y %X'
        )
    else:

        file_handler = CustomTimedRotatingFileHandler(
            filename=log_path,
            app=app,
            when='M',
            interval=1,
            backupCount=0)
        file_handler.setLevel(log_level)

        file_handler.setFormatter(JsonFormatter(app=app, process=process))

        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                file_handler,
                logging.StreamHandler()
            ]
        )

    def my_handler(type, value, tb):
        logging.exception("Uncaught exception: {0}".format(str(value)))

    # Install exception handler
    sys.excepthook = my_handler
