import sys
from loguru import logger
from app.core.config import settings

def setup_logger():
    logger.remove()

    if settings.APP_ENV == 'development':
        logger.add(
            sys.stdout,
            level='DEBUG',
            format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} | {message}'
        )
    else:
        logger.add(
            sys.stdout,
            level='INFO',
            format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} | {message}',
            serialize=True
        )
    logger.add(
        'log/app.log',
        level='ERROR',
        rotation="10 MB",
        retention="30 days",
        serialize=True
    )
    return logger