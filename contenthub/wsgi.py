"""WSGI config for ContentHub2 project."""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contenthub.settings')
application = get_wsgi_application()
