import os

from django.core.wsgi import get_wsgi_application

os.getenv(
    key="DJANGO_SETTINGS_MODULE",
    default="coliving_bot.settings.local"
)

application = get_wsgi_application()
