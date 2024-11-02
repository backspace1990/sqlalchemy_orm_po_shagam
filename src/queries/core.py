from sqlalchemy import text, insert
from database import sync_engine, async_engine
from models import metadata_obj, workers_table


def create_tables():
    sync_engine.echo = True
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = True



def insert_data1():
    with sync_engine.connect() as conn:
        stmt =  """
        INSERT INTO workers(username) VALUES ('Bobr'), ('Volk');"""
        conn.execute(text(stmt))
        conn.commit()


def insert_data():
    with sync_engine.connect() as conn:
        stmt = insert(workers_table).values(
            [
                {'username' : 'BOBR'},
                {'username' : 'VOLK'}

            ])
        conn.execute(stmt)
        conn.commit()