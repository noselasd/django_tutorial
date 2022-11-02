import django_stubs_ext
import socket

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY_WARNING: Set SECRET_KEY for production!
if not SECRET_KEY:
    SECRET_KEY = "not set"

MIDDLEWARE.insert(
    0, "django_browser_reload.middleware.BrowserReloadMiddleware")
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

INSTALLED_APPS.append("debug_toolbar")
INSTALLED_APPS.append("django_browser_reload")

# Set up INTERNAL_IPS for docker etc. to make django-debug-toolbar work.

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

STATIC_ROOT = "/tmp/static"
MEDIA_ROOT = "/tmp/media"


# django_stubs_ext.monkeypatch()
