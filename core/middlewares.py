import logging

from aiohttp.web import middleware
from aiohttp_session import get_session

from core.db import User, user


@middleware
async def user_auth_middleware(request, handler):
    session = await get_session(request)
    db_engine = request.app['db']
    userid = session.get('userid')
    usr = User()  # create anonymous user
    if userid is not None:
        async with db_engine.acquire() as conn:
            user_raw = await conn.execute(user.select().where(user.c.id == userid))
            if user_raw.rowcount > 1:
                logging.error(f'There are multiple users with id: {userid}')
            else:
                user_row = await user_raw.fetchone()
                usr = User(*user_row.as_tuple())

    request['user'] = usr
    resp = await handler(request)
    return resp
