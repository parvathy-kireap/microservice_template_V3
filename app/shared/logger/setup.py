import logging
import sys

from app.app_setup import App


app_logger = logging.getLogger(f'{App.TITLE} Logger')


# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create console handler
console_handler = logging.StreamHandler(stream=sys.stdout)

# set formatter
console_handler.setFormatter(formatter)


# add handlers to logger
app_logger.handlers = [console_handler]

# set log level
app_logger.setLevel(logging.DEBUG)
