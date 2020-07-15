from app.settings.components.base import * # noqa
from app.settings.components.database import * # noqa
# from app.settings.components.email import * # noqa

DEBUG = False


ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')