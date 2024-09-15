import logging

from flask import Blueprint

logger = logging.getLogger(__name__)


class Routes:
    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint

    def add(self, url, view, name=None, log=False):
        name = view.__name__ if name is None else name
        self.blueprint.add_url_rule(url, view_func=view.as_view(name))
