import sys
from loguru import logger
from app.core.config import settings
from contextvars import ContextVar

trace_id_var = ContextVar("trace_id", default="system")
logger = logger.patch(lambda record: record.update(trace_id=trace_id_var.get() or "-"))

def setup_logger():
    logger.remove()

    if settings.APP_ENV == 'development':
        logger.add(
            sys.stdout,
            level='DEBUG',
            format='{trace_id} | {time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} | {message}'
        )
    else:
        logger.add(
            sys.stdout,
            level='INFO',
            format='{trace_id} | {time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} | {message}',
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