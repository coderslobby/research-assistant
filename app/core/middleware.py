import uuid
from app.core.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import trace_id_var
import time

class TraceIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        trace_id_var.set(str(uuid.uuid4()))
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Request processed in {duration:.3f} seconds")
        response.headers["X-Trace-ID"] = trace_id_var.get()
        return response