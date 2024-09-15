import logging
from pathlib import Path

from flask import Blueprint

logger = logging.getLogger(__name__)

base = Path(__file__).resolve().parent
blueprint = Blueprint(
    __name__.replace(".", "_"), __name__
)


@blueprint.errorhandler(Exception)
def page_not_found(e):
    logger.exception(e)
    return 'Error', 500


@blueprint.before_request
def auth():
    ...
