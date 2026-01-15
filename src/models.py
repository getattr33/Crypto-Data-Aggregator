from sqlalchemy import Float, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class TickerPriceORM(Base):
    __tablename__ = "ticker_prices"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(10), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False)
