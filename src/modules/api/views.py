import logging

from dbutils import transactional_cursor, get_conn, get_cursor, Db
from flask.views import MethodView
from flask_pydantic import validate
from psycopg.types.json import Jsonb

from settings import DSN
from .models import CheckRequest, PersistRequest

logger = logging.getLogger(__name__)


class PersistView(MethodView):
    @validate()
    def post(self, body: PersistRequest):
        with transactional_cursor(get_conn(DSN)) as cursor:
            db = Db(cursor=cursor)
            for id in body.ids:
                db.insert("logs", dict(
                    time=id.ts,
                    log_level=id.level,
                    log_text=id.message,
                    extra_data=Jsonb(id.extra),
                    hash=id.hash
                ))
        return True

class CheckView(MethodView):
    @validate()
    def post(self, body: CheckRequest):
        with get_cursor(get_conn(DSN)) as cursor:
            db = Db(cursor=cursor)
            present_ids = db.fetch_all(
                "SELECT hash FROM logs WHERE hash = ANY(%(ids)s)",
                dict(ids=body.ids)
            )
            present_ids = {row['hash'] for row in present_ids}
        return [id for id in body.ids if id not in present_ids]
