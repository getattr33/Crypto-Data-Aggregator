from datetime import datetime, timezone

from src.db_manager import DBManager
from src.schemas.ticker_price_schema import TickerPriceAdd
from src.services.base import BaseService
from src.clients.deribit import DeribitClient


class PriceService(BaseService):
    def __init__(self, db: DBManager | None = None) -> None:
        super().__init__(db)
        self.client = DeribitClient()

    async def fetch_and_save_price(self, ticker: str) -> None:
        price = await self.client.get_index_price(ticker)
        
        timestamp = int(datetime.now(timezone.utc).timestamp())
        await self.db.ticker_price.add(
            TickerPriceAdd(
                ticker=ticker,
                price=price,
                timestamp=timestamp
            )
        )
        await self.db.commit()

