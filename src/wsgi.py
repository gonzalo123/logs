from flask import Flask
from core.logger import setup_logging
from settings import ENVIRONMENT, APP_ID, PROCESS, LOG_PATH
import logging

setup_logging(
    env=ENVIRONMENT,
    app=APP_ID,
    process=PROCESS,
    log_path=LOG_PATH)

logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route("/")
def hello_world():
    logger.info("Hello, World!", extra=dict(gonzalo='xxx'))
    return "<p>Hello, World!</p>"
