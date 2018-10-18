import os
import logging
import asyncio
import yaml
from importlib import import_module

from core.utils import setup_logging
from core.settings import config, get_modules_conf_files


def get_fetcher(conf_filepath):
    with open(conf_filepath) as f:
        fetcher_conf = yaml.load(f)
        module_path = fetcher_conf.get('cloud_fetcher')
        if not module_path:
            logging.error(f'Fetcher module: {module_path} can not be imported')
            return
        del fetcher_conf['cloud_fetcher']
        mod_path, _, class_name = module_path.rpartition('.')
        mod = import_module(mod_path)
        fetcher = getattr(mod, class_name)
        return fetcher(**fetcher_conf)


if __name__ == '__main__':
    setup_logging()

    global_conf = os.getenv('GLOBAL_CONF', './config/global.yml')
    fetchers_conf_files = get_modules_conf_files(config)
    if fetchers_conf_files is None:
        exit(1)

    fetchers = []
    for fetcher_conf_file in fetchers_conf_files:
        fc = get_fetcher(fetcher_conf_file)
        if fc:
            fetchers.append(fc)
    logging.info(f'fetcher_coros: {fetchers}')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(*[f.run() for f in fetchers], return_exceptions=True)
    )
