import os
from enum import Enum
from pathlib import Path

ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')
APP_ID = os.getenv('APP_ID', 'logs')
PROCESS = os.getenv('PROCESS', 'wsgi')

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / 'logs'

LOG_PATH = LOG_DIR / f'{APP_ID}.log.json'

DSN = f"dbname='{os.getenv('DB_NAME')}' user='{os.getenv('DB_USER')}' host='{os.getenv('DB_HOST')}' password='{os.getenv('DB_PASS')}' port='{os.getenv('DB_PORT')}'"
