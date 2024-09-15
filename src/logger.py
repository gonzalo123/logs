from flask import Flask

from core.logger import setup_logging
from settings import ENVIRONMENT, APP_ID, PROCESS, LOG_PATH
import logging
from modules.api.urls import blueprint as logger_blueprint

setup_logging(
    env=ENVIRONMENT,
    app=APP_ID,
    process=PROCESS,
    log_path=LOG_PATH)


logger = logging.getLogger(__name__)
app = Flask(__name__)

app.register_blueprint(logger_blueprint, url_prefix=f'/{APP_ID}/api')
