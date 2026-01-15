from src.models import TickerPriceORM
from src.schemas.ticker_price_schema import TickerPrice
from src.repositories.base import BaseRepository


class TickerPriceRepository(BaseRepository):
    model = TickerPriceORM
    schema = TickerPrice