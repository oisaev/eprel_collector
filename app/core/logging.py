import logging
import logging.config
import os
from pathlib import Path

from core.settings import settings


log_path = Path(settings.logging_dir)
if not os.path.exists(log_path):
    os.makedirs(log_path)

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'level': logging.INFO,
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.INFO,
            'formatter': 'default',
            'filename': log_path / 'eprel_scraper.log',
            'maxBytes': 10_000_000,
            'backupCount': 5,
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '': {
            'handlers': ['stdout', 'file'],
            'level': logging.INFO,
            'propagate': True,
        }
    },
    'disable_existing_loggers': False,
}

logging.config.dictConfig(LOGGING)

logger = logging.getLogger(__name__)
