from app.settings.components.base import * # noqa
from app.settings.components.database import * # noqa
from app.settings.components.dev_tools import * # noqa

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'cdn/static')
