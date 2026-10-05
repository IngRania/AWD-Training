"""Notification microservice - entry point.

Run:  uvicorn app.main:app --reload --port 8084
  or: python -m app.main
"""
import logging
import os
from contextlib import asynccontextmanager

import py_eureka_client.eureka_client as eureka_client
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers import notification

logger = logging.getLogger("notification")

PORT = int(os.getenv("PORT", "8084"))
EUREKA_ENABLED = os.getenv("EUREKA_ENABLED", "true").lower() == "true"
EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Register with Eureka at startup, deregister at shutdown."""
    registered = False
    if EUREKA_ENABLED:
        try:
            await eureka_client.init_async(
                eureka_server=EUREKA_SERVER,
                app_name="notification",
                instance_host="localhost",
                instance_port=PORT,
            )
            registered = True
            logger.info("Registered with Eureka at %s", EUREKA_SERVER)
        except Exception as exc:  # the service must still start without Eureka
            logger.warning("Eureka registration failed: %s", exc)
    yield
    if registered:
        await eureka_client.stop_async()


app = FastAPI(
    lifespan=lifespan,
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    # Same URLs as the other microservices of the project
    docs_url="/swagger-ui",       # Swagger UI
    openapi_url="/v3/api-docs",   # OpenAPI JSON
    redoc_url="/redoc",           # alternative documentation
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/swagger-ui")


app.include_router(notification.router)

# TODO (students): if you add other routers, include them here.


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)