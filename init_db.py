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
    try:
        create_tables(engine=engine, tables=tables_to_create)
    except OperationalError:
        sleep(timeout)   # sleep till time when docker connect db
