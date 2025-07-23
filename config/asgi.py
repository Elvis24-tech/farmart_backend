# config/asgi.py
import os
from django.core.asgi import get_asgi_application

# This points to your settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

application = get_asgi_application()