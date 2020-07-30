from app.settings.components.base import * # noqa
from app.settings.components.database import * # noqa
from app.settings.components.email import * # noqa

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

STATIC_ROOT = '/var/www/tmb/static'

MEDIA_ROOT = '/var/www/tmb/media'
