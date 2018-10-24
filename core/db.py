import logging
from dataclasses import dataclass
from typing import NamedTuple

import asyncio
from aiopg.sa import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, BIGINT
from sqlalchemy.dialects.postgresql import HSTORE, TIMESTAMP
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects.postgresql import insert


# Tables

meta = MetaData()

user = Table(
    'user', meta,
    Column('id', BIGINT, primary_key=True),
    Column('username', String(100), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('profile_url', String(300)),
    Column('avatar_url', String(500)),
)

account = Table(
    'account', meta,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('access_token', String(500)),
    Column('refresh_token', String(500)),
    Column('expires', TIMESTAMP),
    Column('raw_data', HSTORE),
)

# tables to create on the first run
tables_to_create = [user, account]

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


@dataclass
class User:
    id: int = -1
    username: str = ''
    profile_url: str = ''
    avatar_url: str = ''
    email: str = ''

    @property
    def is_anonymous(self):
        return self.id == -1

    async def save_to_db(self, db_engine):
        global user
        if not db_engine:
            logging.error("An empty db engine")
            return
        async with db_engine.acquire() as conn:
            inserted_usr = await conn.execute(
                insert(user).returning(user.c.id).values(
                    username=self.username,
                    email=self.email,
                    profile_url=self.profile_url,
                    avatar_url=self.avatar_url,
                ).on_conflict_do_nothing(
                    index_elements=['email']
                )
            )

            # inserted_usr = await conn.execute(insert_usr_stmt)
            inserted_usr_row = await inserted_usr.fetchone()
            if inserted_usr_row:
                self.id = inserted_usr_row.get('id', 0)
            else:
                # get is from existing row
                current_id = await conn.execute(
                    user.select().where(user.c.email == self.email)
                )
                current_id_row = await current_id.fetchone()
                self.id = current_id_row.get('id', 0)



