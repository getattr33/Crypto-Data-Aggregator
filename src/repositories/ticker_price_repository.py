from sqlalchemy import select
from src.models import TickerPriceORM
from src.schemas.ticker_price_schema import TickerPriceBase
from src.repositories.base import BaseRepository


class TickerPriceRepository(BaseRepository):
    model = TickerPriceORM
    schema = TickerPriceBase

    async def get_by_date(
        self, ticker: str, from_ts: int | None = None, to_ts: int | None = None
    ):
        """
        Возвращает все записи для указанного тикера в диапазоне timestamp.
        """
        query = select(self.model).filter_by(ticker=ticker)

        if from_ts is not None:
            query = query.filter(self.model.timestamp >= from_ts)
        if to_ts is not None:
            query = query.filter(self.model.timestamp <= to_ts)

        result = await self.session.execute(query)
        return result.scalars().all()
