import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - [%(correlation_id)s] - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

class BeforeAfterLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate or propagate Correlation ID
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        # Start logging the request
        logger.info(
            f"Request received: {request.method} {request.url} - Correlation ID: {correlation_id}",
            extra={"correlation_id": correlation_id},
        )

        # Measure request processing time
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Add Correlation ID to the response headers
        response.headers["X-Correlation-ID"] = correlation_id

        # Log the response details
        logger.info(
            f"Request completed: {request.method} {request.url} - Correlation ID: {correlation_id} - "
            f"Processed in {process_time:.2f} seconds",
            extra={"correlation_id": correlation_id},
        )

        # Add processing time to the response header (optional)
        response.headers["X-Process-Time"] = str(process_time)

        return response
