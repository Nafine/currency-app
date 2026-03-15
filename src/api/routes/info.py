from datetime import date as datetime_date
from typing import Any

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import HTTPException, APIRouter

from src.models import SettingsPublic, ServiceInfoPublic
from src.service.currency_service import CurrencyService
from src.config.config import Settings

router = APIRouter(route_class=DishkaRoute)


@router.get("/info")
async def read_info(cfg: FromDishka[Settings]) -> SettingsPublic:
    return SettingsPublic(
        version=cfg.version,
        service=cfg.service,
        author=cfg.author,
    )


@router.get("/info/currency", response_model=ServiceInfoPublic)
async def read_currency(service: FromDishka[CurrencyService], currency: str | None = None,
                        date: datetime_date | None = None) -> Any:
    if not currency:
        return ServiceInfoPublic(service="currency", data=service.get_rates_map(date))

    try:
        rate = service.get_currency_rate(date, currency)
        return ServiceInfoPublic(service="currency", data={currency.upper(): rate})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
