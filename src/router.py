from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from src.db_manager import DBManager
from src.database import async_session_maker


from datetime import date

from fastapi import APIRouter, Query

from src.schemas.ticker_price_schema import Ticker, TickerPriceRead
from src.services.ticker_price_service import PriceService


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]

router = APIRouter(prefix="/prices", tags=["Цены криптовалют"])


@router.get(
    "/all",
    summary="Получение всех сохранённых данных по валюте",
    description="""Возвращает все сохранённые значения цены для указанной валюты.

Используется для анализа исторических данных.

Обязательные параметры:
- ticker — тикер валюты (например btc_usd, eth_usd)
""",
    response_model=list[TickerPriceRead],
    responses={
        200: {"description": "Список всех сохранённых цен"},
        404: {"description": "Данные по валюте не найдены"},
        422: {"description": "Некорректные параметры"},
    },
)
async def get_all_prices(
    ticker: Ticker = Query(..., description="Тикер валюты (btc_usd, eth_usd)"),
    db: DBDep = None,
):
    prices = await PriceService(db).get_all_prices(ticker=ticker.value)
    if not prices:
        raise HTTPException(
            status_code=404, detail="Цены для указанной валюты не найдены"
        )
    return prices


@router.get(
    "/latest",
    summary="Получение последней цены валюты",
    description="""Возвращает последнюю сохранённую цену для указанной валюты.

Используется для отображения актуального курса.

Обязательные параметры:
- ticker — тикер валюты
""",
    response_model=TickerPriceRead,
    responses={
        200: {"description": "Последняя цена валюты"},
        404: {"description": "Цена для валюты не найдена"},
        422: {"description": "Некорректные параметры"},
    },
)
async def get_latest_price(
    ticker: Ticker = Query(..., description="Тикер валюты (btc_usd, eth_usd)"),
    db: DBDep = None,
):
    prices = await PriceService(db).get_latest_price(ticker=ticker.value)
    if prices is None:
        raise HTTPException(
            status_code=404, detail="Цены для указанной валюты не найдены"
        )
    return prices


@router.get(
    "/by-date",
    summary="Получение цены валюты с фильтром по дате",
    description="""Возвращает цены валюты за указанный период.

Можно использовать:
- только from_date
- только to_date
- обе даты одновременно

Если даты не указаны — возвращаются все данные по валюте.

Обязательные параметры:
- ticker — тикер валюты
""",
    response_model=list[TickerPriceRead],
    responses={
        200: {"description": "Список цен за указанный период"},
        404: {"description": "Данные за период не найдены"},
        422: {"description": "Некорректные параметры"},
    },
)
async def get_prices_by_date(
    ticker: Ticker = Query(..., description="Тикер валюты (btc_usd, eth_usd)"),
    from_date: date | None = Query(None, description="Начальная дата (YYYY-MM-DD)"),
    to_date: date | None = Query(None, description="Конечная дата (YYYY-MM-DD)"),
    db: DBDep = None,
):
    prices = await PriceService(db).get_prices_by_date(
        ticker=ticker.value,
        from_date=from_date,
        to_date=to_date,
    )
    if not prices:
        raise HTTPException(
            status_code=404, detail="Цены для указанной валюты не найдены"
        )
    return prices
