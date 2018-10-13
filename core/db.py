from aiopg.sa import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.schema import CreateTable

# Tables

meta = MetaData()

user = Table(
    'user', meta,
    Column('id', Integer, primary_key=True),
    Column('username', String(100), nullable=False),
    Column('email', String(100), nullable=False),
)

tables_to_create = [user]
# End tables

async def create_tables(engine, tables):
    async with engine.acquire() as conn:
        for table in tables:
            create_expr = CreateTable(table)
            await conn.execute(create_expr)


async def init_db(app):
    db_conf = app['config']['db']
    engine = await create_engine(**db_conf)
    app['db'] = engine


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()


