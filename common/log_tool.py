# coding=utf-8
import logging
from blog import settings
import os

logger = None

def get_logger():
    global logger
    if not logger:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        try:
            if os.environ['IN_DJANGO_DEV_MODE']:
                return logger
        except:
            pass
        from bae_log import handlers
        handler = handlers.BaeLogHandler(ak = settings.BAE_APP_KEY, sk = settings.BAE_SECRET_KEY, bufcount=128)
        logger.addHandler(handler)
        logger.debug('Logger is running!')
    return logger