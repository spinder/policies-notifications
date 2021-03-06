# Standard library
import logging

# Third-party
from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware

# Local
from .routers import apps, endpoints
from .db.conn import db
from .events import consume, email
from .core.config import TESTING
from .core.logging import PrometheusAccessLogFilter

logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    # KafkaConsumers
    consumer = consume.EventConsumer()
    email_consumer = email.EmailSubscriptionConsumer()

    # ASGi
    notif_app: FastAPI = FastAPI(title='Notifications backend', openapi_url='/api/v1/openapi.json', redoc_url=None)
    db.init_app(notif_app)

    notif_app.add_middleware(PrometheusMiddleware)
    notif_app.add_route("/metrics", metrics)
    notif_app.include_router(apps.apps, tags=['Apps'])
    notif_app.include_router(endpoints.endpoints, tags=['Endpoints'])

    @notif_app.on_event("startup")
    async def startup_event():
        logger.info('Starting Notifications backend')
        # await conn.setup()
        if not TESTING:
            await consumer.start()
            await email_consumer.start()
        logger.info('Notifications backend started')

    @notif_app.on_event("shutdown")
    async def shutdown_event():
        logger.info('Shutting down Notifications backend')
        # await conn.shutdown()
        if not TESTING:
            await consumer.shutdown()
            await email_consumer.shutdown()
        logger.info('Notifications backend shutdown complete')

    return notif_app


def config_logging():
    p = PrometheusAccessLogFilter()
    logging.getLogger('uvicorn.access').addFilter(p)


notif_app = get_app()
config_logging()
