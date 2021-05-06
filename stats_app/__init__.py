from stats_app.dash_app import app
import logging


# Set waitress server logging level to ERROR
logger = logging.getLogger('waitress')
logger.setLevel(logging.ERROR)

print('Running at http://0.0.0.0:8080 (default)')
server = app.server
