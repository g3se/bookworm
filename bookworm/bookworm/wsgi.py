"""
WSGI config for bookworm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

# ---BEGIN configuration from PythonAnywhere
# --- <https://help.pythonanywhere.com/pages/FollowingTheDjangoTutorial>
import os
import sys


path = os.path.expanduser('~/bookworm/bookworm')
if path not in sys.path:
    sys.path.insert(0, path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(get_wsgi_application())
# ---END configuration from PythonAnywhere



# ---BEGIN default configuration
# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookworm.settings")

# application = get_wsgi_application()
# ---END default configuration
