import os

import yaml
import logging.config

from aiohttp.web_exceptions import HTTPFound
from aiohttp_session import get_session


def setup_logging(logger_cfg='./config/default_logger.yml', env_key='LOGGER_CFG'):
    path = logger_cfg
    env_conf = os.getenv(env_key, None)
    if env_conf:
        path = env_conf
    if os.path.isfile(path):
        with open(path) as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)


def login_required(func):
    async def wrapper(*args, **kwargs):
        request, *_ = args
        session = await get_session(request)
        # raise HTTPFound('/login')
        return await func(*args, **kwargs)
    return wrapper