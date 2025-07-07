import logging
from datetime import datetime, timezone
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.auth.services import AuthService
from app.auth.utils.token_utils import get_token_expiration
from app.settings import settings

logger = logging.getLogger(__name__)


class AutoTokenRefreshMiddleware(BaseHTTPMiddleware):
    """Middleware to automatically update tokens upon expiration"""

    def __init__(self, app, skip_paths: list[str], refresh_threshold_minutes: int = 5):
        super().__init__(app)
        self.refresh_threshold = refresh_threshold_minutes * 60
        self.skip_paths = skip_paths

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if any(request.url.path.startswith(path) for path in self.skip_paths):
            return await call_next(request)

        access_token = (request.headers.get("Authorization") or "").replace(
            "Bearer ", ""
        )
        refresh_token = request.cookies.get("refresh_token", "")

        if not access_token:
            return await call_next(request)

        response = await call_next(request)

        try:
            exp_time = get_token_expiration(access_token)
            if not exp_time:
                return response

            current_time = datetime.now(timezone.utc)
            time_until_exp = (exp_time - current_time).total_seconds()

            if time_until_exp < self.refresh_threshold and refresh_token:
                db = next(settings.get_db())
                try:
                    auth_service = AuthService(db)
                    refresh_response = await auth_service.refresh_tokens(refresh_token)
                    new_access_token = refresh_response.access_token

                    if new_access_token:
                        response.headers["X-New-Access-Token"] = new_access_token
                        response.headers["X-Token-Refreshed"] = "true"
                        logger.info(f"Token auto-refreshed for {request.url.path}")

                finally:
                    db.close()

        except Exception as e:
            logger.warning(f"Token refresh failed: {e}")

        return response
