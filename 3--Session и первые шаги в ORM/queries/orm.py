from sqlalchemy import text, insert
from database import sync_engine, async_engine, session_faktory, Base, asyn_session_faktory
from models import metadata_obj, workers_table, WorkersOrm


def create_tables():
    sync_engine.echo = True
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True


#def asyn_create_tables():
#    async_engine.echo = True
#    Base.metadata.drop_all(async_engine)
#    Base.metadata.create_all(async_engine)
#    async_engine.echo = True


def insert_data():
    with session_faktory() as session:
        workers_bobr = WorkersOrm(username="Bobr")
        workers_volk = WorkersOrm(username="Volk")
        session.add_all([workers_bobr, workers_volk])
        session.commit()


"""
for async sess 
"""
async def asyn_insert_data():
    async with asyn_session_faktory() as asyn_session:
        workers_bobr = WorkersOrm(username="Bobr")
        workers_volk = WorkersOrm(username="Volk")
        asyn_session.add_all([workers_bobr, workers_volk])
        await asyn_session.commit()