import pathlib
import yaml
import os

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
BASE_DIR = pathlib.Path(__file__).parent.parent
env_path = pathlib.Path(os.getenv('CONFIG_PATH')) if os.getenv('CONFIG_PATH') else None
config_path = env_path or BASE_DIR / 'config' / 'global.yml'


def get_config(path):
    if config_path.exists():
        with open(path) as f:
            config = yaml.load(f)
        return config
    exit(f"Config file is missing in path: {path}")

config = get_config(config_path)