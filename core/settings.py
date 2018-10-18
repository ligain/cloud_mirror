import logging
import pathlib
import yaml
import os

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
BASE_DIR = pathlib.Path(__file__).parent.parent
env_path = pathlib.Path(os.getenv('CONFIG_PATH')) if os.getenv('CONFIG_PATH') else None
config_path = env_path or BASE_DIR / 'config' / 'global.yml'


class MissingConfigFile(Exception):
    pass


def get_config(path):
    if config_path.exists():
        with open(path) as f:
            config = yaml.load(f)
        return config
    raise MissingConfigFile(f"Global config file is missing in path: {path}")


def get_modules_conf_files(global_conf=None):
    modules_conf = global_conf.get('fetchers')
    if not modules_conf:
        raise KeyError('There are no fetchers in global config')

    modules_path = pathlib.Path(modules_conf.get('config_dir', '')).resolve()
    modules_conf_dirs = os.listdir(modules_path)
    if not modules_conf_dirs:
        raise MissingConfigFile(f"Not fetchers configs was found in: {modules_path}")

    for module_conf_dir in modules_conf_dirs:
        yield pathlib.PurePosixPath(modules_path).joinpath(module_conf_dir)


def get_modules_config(global_conf):
    modules_config = {}
    if not global_conf:
        raise ValueError('Missing global config object')
    modules_conf_files = get_modules_conf_files(global_conf)
    for module_conf_file in modules_conf_files:
        try:
            module_file_name = module_conf_file.parts[-1]
            module_name = module_file_name.split('.')[0]
            with open(module_conf_file) as f:
                modules_config[module_name] = yaml.load(f)
        except FileNotFoundError:
            logging.exception(f"File: {module_conf_file} is missing")
            continue
        except yaml.YAMLError:
            logging.exception(f"Invalid yaml file: {module_conf_file}")
            continue
    return modules_config


config = get_config(config_path)
modules_config = get_modules_config(config)
google_drive_secrets_file = os.getenv('GOOGLE_DRIVE_CREDENTIALS_FILE') or \
                            modules_config['google_drive']['credentials_file']