import os
import yaml
import logging.config


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