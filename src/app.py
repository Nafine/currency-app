from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.setup.app_factory import create_web_app, create_ioc_container


def make_app() -> FastAPI:
    app = create_web_app()
    container = create_ioc_container()
    setup_dishka(container, app)

    return app
