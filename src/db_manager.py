from src.repositories.ticker_price_repository import TickerPriceRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.ticker_price = TickerPriceRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def begin(self):
        await self.session.begin()

    async def rollback(self):
        await self.session.rollback()
