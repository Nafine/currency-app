from dishka import make_async_container, AsyncContainer

from src.config.config import SettingsProvider
from src.parser.xml_parser import CurrencyXmlParseProvider
from src.service.currency_service import CurrencyServiceProvider


def create_app_container() -> AsyncContainer:
    return make_async_container(CurrencyServiceProvider(), SettingsProvider(), CurrencyXmlParseProvider())
