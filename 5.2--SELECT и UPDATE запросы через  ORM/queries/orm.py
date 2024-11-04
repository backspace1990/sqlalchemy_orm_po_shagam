from sqlalchemy import text, insert, select, update
from database import sync_engine, async_engine, session_faktory, Base, asyn_session_faktory
from models import metadata_obj, workers_table, WorkersOrm


class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_data():
        with session_faktory() as session:
            workers_bobr = WorkersOrm(username="Bobr")
            workers_volk = WorkersOrm(username="Volk")
            session.add_all([workers_bobr, workers_volk])
            session.commit()
    
    @staticmethod
    def select_workers():
        with session_faktory() as session:
            #worker_id = 1
            #worker_Jack = session.get(WorkersOrm, worker_id)
            query = select(WorkersOrm) 
            result = session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")


    @staticmethod
    def update_workers(worker_id: int = 1, new_username: str = "LEVENT"):
        with session_faktory() as session:
            worker_jack = session.get(WorkersOrm, worker_id)
            worker_jack.username = new_username
            session.commit()
