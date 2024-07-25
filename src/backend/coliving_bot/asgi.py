import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="coliving_bot.settings.stage")

application = get_asgi_application()
