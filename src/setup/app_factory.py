from collections.abc import Iterable

from dishka import AsyncContainer, Provider, make_async_container
from fastapi import FastAPI

from src.api.main import create_root_router
from src.config.config import SettingsProvider
from src.parser.xml_parser import CurrencyXmlParseProvider
from src.service.currency_service import CurrencyServiceProvider


def create_web_app() -> FastAPI:
    app = FastAPI()

    app.include_router(create_root_router())

    return app


def create_ioc_container() -> AsyncContainer:
    return make_async_container(*get_providers())


def get_providers() -> Iterable[Provider]:
    return CurrencyServiceProvider(), SettingsProvider(), CurrencyXmlParseProvider()
