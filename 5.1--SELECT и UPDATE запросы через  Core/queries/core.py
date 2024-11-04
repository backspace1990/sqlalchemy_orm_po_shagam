from sqlalchemy import text, insert, select, update
from database import sync_engine, async_engine
from models import metadata_obj, workers_table


def create_tables():
    sync_engine.echo = True
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = True


class SyncCore:
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with sync_engine.connect() as conn:
            #stmt =  """
            #    INSERT INTO workers(username) VALUES ('Bobr'), ('Volk');"""
            stmt = insert(workers_table).values(
                [
                    {'username' : 'BOBR'},
                    {'username' : 'VOLK'}
                ]
            )
            conn.execute(stmt)
            conn.commit()
    
    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            query = select(workers_table) # SELECT * FROM workers
            result = conn.execute(query)
            #result2 = conn.execute(query)
            #workers_id = result2.scalars().all()
            #print(f"{workers_id=}")
            workers = result.all()
            print(f"{workers=}")
    
    @staticmethod
    def update_worker(worker_id: int=2, new_username: str = "Volkan"):
        with sync_engine.connect() as conn:
            stmt = text("UPDATE workers SET username=:username WHERE id=:id")
            stmt = stmt.bindparams(username=new_username, id=worker_id)
            conn.execute(stmt)
            conn.commit()
    
    @staticmethod
    def update_worker_sqlal_po_func(worker_id: int=1, new_username: str = "Ümit"):
        with sync_engine.connect() as conn:
            stmt = (
                update(workers_table)
                .values(username=new_username)
                #.where(workers_table.c.id==worker_id)
                .filter_by(id=worker_id)
            )
            conn.execute(stmt)
            conn.commit()
        
