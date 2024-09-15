from core.flask_api import Routes

from . import blueprint
from .views import CheckView, PersistView


r = Routes(blueprint)

r.add("/check", CheckView)
r.add("/persist", PersistView)
