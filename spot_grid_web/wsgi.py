"""
WSGI config for spot_grid_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spot_grid_web.settings')

application = get_wsgi_application()


from apscheduler.schedulers.background import BackgroundScheduler


from tasks import SpotGridViews
from spot_grid_web import settings, private_settings

# import logging
#
# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)
spot = SpotGridViews()
scheduler.add_job(spot.spot_start_run, "interval", seconds=private_settings.interval_time, id="spot_grid_run", replace_existing=True)

scheduler.start()
