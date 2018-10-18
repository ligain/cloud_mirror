import os
import pytest

from core.settings import modules_config
from modules.google_drive.token_manager import GoogleDriveTokenManager


@pytest.fixture
def token_manager():
    cfg = modules_config['google_drive']
    credentials_file_path = os.getenv('GOOGLE_DRIVE_CREDENTIALS_FILE')
    return GoogleDriveTokenManager(
        credentials_file=credentials_file_path,
        scopes=cfg.get('scopes', [])
    )


def test_parse_credentials_file(token_manager):
    token_manager.get_credentials_from_file()
    assert 1 == 1