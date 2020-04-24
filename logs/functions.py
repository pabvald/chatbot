import os
import logging
from logging.handlers import  RotatingFileHandler


def init_log(app):
    """ Configures rotating log file for the Project """
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        handler = RotatingFileHandler('logs/bot.log', maxBytes=20480, backupCount=20)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Bot startup')