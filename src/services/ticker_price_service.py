from datetime import datetime, timezone

from src.db_manager import DBManager
from src.schemas.ticker_price_schema import TickerPriceAdd
from src.services.base import BaseService
from src.clients.deribit import DeribitClient
from datetime import date, datetime


class PriceService(BaseService):
    def __init__(self, db: DBManager | None = None) -> None:
        super().__init__(db)
        self.client = DeribitClient()

    async def fetch_and_save_price(self, ticker: str) -> None:
        price = await self.client.get_index_price(ticker)

        timestamp = int(datetime.now(timezone.utc).timestamp())
        await self.db.ticker_price.add(
            TickerPriceAdd(ticker=ticker, price=price, timestamp=timestamp)
        )
        await self.db.commit()

    async def get_all_prices(self, ticker: str):
        return await self.db.ticker_price.get_all(ticker=ticker)

    async def get_latest_price(self, ticker: str):
        return await self.db.ticker_price.get_latest(ticker=ticker)

    async def get_prices_by_date(
        self,
        ticker: str,
        from_date: date | None = None,
        to_date: date | None = None,
    ):
        from_ts = (
            int(datetime.combine(from_date, datetime.min.time()).timestamp())
            if from_date
            else None
        )
        to_ts = (
            int(datetime.combine(to_date, datetime.max.time()).timestamp())
            if to_date
            else None
        )

        prices = await self.db.ticker_price.get_by_date(
            ticker=ticker,
            from_ts=from_ts,
            to_ts=to_ts,
        )

        return prices
