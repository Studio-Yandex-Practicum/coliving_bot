import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="coliving_bot.settings.stage")

application = get_wsgi_application()
