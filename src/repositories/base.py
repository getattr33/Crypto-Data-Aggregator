from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError




class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *filter, **filter_by):
        query = select(self.model).filter_by(**filter_by).filter(*filter)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return model

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return model

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return model







