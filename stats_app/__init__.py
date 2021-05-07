from stats_app.dash_app import app
import logging


# Set waitress.queue logging level to ERROR
logging.getLogger('waitress.queue').setLevel(logging.ERROR)

server = app.server
