from pydantic import BaseModel
import enum


class Ticker(str, enum.Enum):
    BTC_USD = "btc_usd"
    ETH_USD = "eth_usd"


class TickerPriceBase(BaseModel):
    ticker: Ticker
    price: float
    timestamp: int


class TickerPriceAdd(TickerPriceBase):
    pass


class TickerPriceRead(TickerPriceBase):
    id: int

    class Config:
        from_attributes = True
