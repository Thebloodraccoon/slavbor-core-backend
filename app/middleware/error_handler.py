from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def setup_error_handlers(app):
    """Setting a global error handler for Fastapi application."""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """The processor of all HTTP exceptions including your custom."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "status_code": exc.status_code,
                    "detail": exc.detail,
                    "type": type(exc).__name__,
                }
            },
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        """Pydantic validation error processor."""
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "status_code": 422,
                    "detail": "Validation failed",
                    "type": "ValidationError",
                    "validation_errors": [
                        {
                            "field": ".".join(str(loc) for loc in error["loc"]),
                            "message": error["msg"],
                            "type": error["type"],
                        }
                        for error in exc.errors()
                    ],
                }
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """SQLCHEMY error handler."""

        if isinstance(exc, IntegrityError):
            error_detail = "Database integrity constraint violation"
            status_code = 400

            error_str = str(exc.orig) if hasattr(exc, "orig") else str(exc)
            if "UNIQUE" in error_str.upper():
                error_detail = "Record with this data already exists"
            elif "FOREIGN KEY" in error_str.upper():
                error_detail = "Referenced record does not exist"
            elif "NOT NULL" in error_str.upper():
                error_detail = "Required field cannot be empty"
        else:
            error_detail = "Database operation failed"
            status_code = 500

        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "status_code": status_code,
                    "detail": error_detail,
                    "type": "DatabaseError",
                }
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global handler of all unprocessed exceptions."""

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "status_code": 500,
                    "detail": "Internal server error",
                    "type": type(exc).__name__,
                }
            },
        )
