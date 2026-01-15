from pydantic import BaseModel, Field


class TickerPriceAdd(BaseModel):
    ticker: str = Field(min_length=1, max_length=10)
    price: float
    timestamp: int = Field(gt=0)

class TickerPrice(TickerPriceAdd):
    id: int