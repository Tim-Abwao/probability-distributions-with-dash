import logging

from distributions_dashboard.dash_app import app

# Set waitress.queue logging level to ERROR
logging.getLogger("waitress.queue").setLevel(logging.ERROR)

server = app.server
