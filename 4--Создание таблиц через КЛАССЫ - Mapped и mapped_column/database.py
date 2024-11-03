import asyncio
from sqlalchemy import String, create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from config import settings
from typing import Annotated



sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    #pool_size=5,    #baglanti sayisi
    #max_overflow=10  #yukaridaki baglanti sayisi dolunca ekstra 10 baglanti daha saglar
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    
)



session_faktory = sessionmaker(sync_engine)
asyn_session_faktory = async_sessionmaker(async_engine)



str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }




#with sync_engine.connect() as conn:
#    res = conn.execute(text("SELECT VERSION()"))
#    print(f"{res.first()=}")


#async def get_123():
#    async with async_engine.connect() as conn:
#        res = await conn.execute(text("SELECT VERSION()"))
#        print(f"{res.first()=}")


#asyncio.run(get_123())