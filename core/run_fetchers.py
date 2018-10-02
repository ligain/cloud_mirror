import os
import logging
import asyncio
import yaml
from pathlib import PurePosixPath, Path
from importlib import import_module

from core.utils import setup_logging


def get_fetchers_conf_files(global_conf_file=None):
    if not global_conf_file:
        logging.error('You should specify path to global config')
        return

    with open(global_conf_file) as f:
        global_conf = yaml.load(f)
    fetchers_conf = global_conf.get('fetchers')
    if not fetchers_conf:
        logging.error('Fetchers config dir was not found in global config')
        return

    fetchers_path = Path(fetchers_conf.get('config_dir', '')).resolve()
    fetchers_conf_dirs = os.listdir(fetchers_path)
    if not fetchers_conf_dirs:
        logging.error('Not fetchers configs was found')
        return

    for fetcher_conf_dir in fetchers_conf_dirs:
        yield PurePosixPath(fetchers_path).joinpath(fetcher_conf_dir)


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
    fetchers_conf_files = get_fetchers_conf_files(global_conf)
    if fetchers_conf_files is None:
        exit(1)

    fetchers = []
    for fetcher_conf_file in fetchers_conf_files:
        fc = get_fetcher(fetcher_conf_file)
        if fc:
            fetchers.append(fc)
    logging.info(f'fetcher_coros: {fetchers}')

    asyncio.run(
        asyncio.wait([f.run() for f in fetchers])
    )
