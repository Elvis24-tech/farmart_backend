# config/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

# This points to your settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

application = get_wsgi_application()