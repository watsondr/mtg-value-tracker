"""
WSGI config for MTGDeckValueTracker project.

Found Here:
https://www.codementor.io/@aswinmurugesh/deploying-a-django-application-in-windows-with-apache-and-mod_wsgi-uhl2xq09e
"""

activate_this = 'D:/Programs/Dropbox/Cross Computer Coding/Python Projects/MTGDeckValueTracker/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site
from django.core.wsgi import get_wsgi_application

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('D:/Programs/Dropbox/Cross Computer Coding/Python Projects/MTGDeckValueTracker/Lib/site-packages')




# Add the app's directory to the PYTHONPATH
sys.path.append('D:/Programs/Dropbox/Cross Computer Coding/Python Projects/MTGDeckValueTracker/')
sys.path.append('D:/Programs/Dropbox/Cross Computer Coding/Python Projects/MTGDeckValueTracker/MTGDeckValueTracker/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'MTGDeckValueTracker.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MTGDeckValueTracker.settings")

application = get_wsgi_application()