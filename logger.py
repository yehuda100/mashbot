import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
file_handler = logging.FileHandler('mash_bot.log')
file_handler.setLevel(logging.INFO)

# create a stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)