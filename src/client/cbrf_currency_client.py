from datetime import date as datetime_date
from typing import List

import httpx

from src.client.currency_client import CurrencyClient
from src.models import Currency
from src.parser.currency_parser import CurrencyParser


class CbrfCurrencyClient(CurrencyClient):
    _CBRF_BASE_URL = "https://www.cbr.ru/scripts/XML_daily.asp"

    def __init__(self, currency_parser: CurrencyParser):
        self._currency_parser = currency_parser

    def get_daily_rates(self, date: datetime_date | None = None) -> List[Currency]:
        return self._currency_parser.parse_all(self._fetch_daily_rates(date))

    def get_rates_map(self, date: datetime_date | None = None) -> dict[str, float]:
        return self._currency_parser.parse_rates(self._fetch_daily_rates(date))

    @classmethod
    def _fetch_daily_rates(cls, date: datetime_date | None = None) -> str:
        params = {"date_req": date.strftime('%d/%m/%Y')} if date else None
        return httpx.get(cls._CBRF_BASE_URL, params=params).text
