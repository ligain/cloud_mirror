from core.settings import config
from core.db import tables_to_create
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError
from time import sleep

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine, tables):
    meta = MetaData()
    meta.create_all(bind=engine, tables=tables)


if __name__ == '__main__':
    timeout = 5
    db_uri = DSN.format(**config['db'])
    engine = create_engine(db_uri)

    # add hstore extension
    with engine.begin() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS HSTORE;")

    try:
        create_tables(engine=engine, tables=tables_to_create)
    except OperationalError as e:
        print(f'Error: {e} on connection to DB. Sleep for {timeout} sec')
        sleep(timeout)   # sleep till time when docker connect db
