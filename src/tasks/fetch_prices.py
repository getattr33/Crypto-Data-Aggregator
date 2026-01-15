import asyncio
from src.tasks.celery_app import celery_app
from src.services.ticker_price_service import PriceService
from src.db_manager import DBManager
from src.database import async_session_maker_null_pооl


@celery_app.task(name="fetch_prices_task")
def fetch_prices_task() -> None:
    asyncio.run(_run())


async def _run() -> None:
    async with DBManager(session_factory=async_session_maker_null_pооl) as db:
        service = PriceService(db=db)
        await service.fetch_and_save_price(ticker="btc_usd")
        await service.fetch_and_save_price(ticker="eth_usd")
