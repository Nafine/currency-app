from datetime import date as datetime_date

from dishka import Provider, Scope, provide

from src.client.cbrf_currency_client import CbrfCurrencyClient
from src.client.currency_client import CurrencyClient
from src.parser.xml_parser import CurrencyXmlParser


class CurrencyService:
    def __init__(self, currency_client: CurrencyClient):
        self._currency_client = currency_client

    def get_currency_rate(self, date: datetime_date | None = None, currency: str | None = None) -> float:
        rates = self._currency_client.get_rates_map(date=date)

        if len(rates) == 0:
            raise ValueError(f'No rates found for {date}')

        try:
            return rates[currency.upper()]
        except KeyError as e:
            raise ValueError(f"Invalid currency: {currency}") from e

    def get_rates_map(self, date: datetime_date | None = None) -> dict[str, float]:
        return self._currency_client.get_rates_map(date=date)


class CurrencyServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def create_service(self) -> CurrencyService:
        return CurrencyService(CbrfCurrencyClient(CurrencyXmlParser()))
