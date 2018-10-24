import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import httplib2

from core.db import account
from core.settings import MissingConfigFile
from oauth2client import file, client, tools
import google_auth_httplib2
from google.oauth2.credentials import Credentials


@dataclass
class GoogleDriveTokenManager:
    access_token: str
    refresh_token: str
    expires: datetime
    token_uri: str
    # def __init__(self, access_token, refresh_token, expires, token_uri):
    #     self.access_token = access_token
    #     self.refresh_token = refresh_token
    #     self.expires = expires
    #     self.token_uri = token_uri


    # def __init__(self, credentials: Credentials):
    #     self.credentials = credentials

    def get_tokens(self):
        pass

    def check_access_token(self):
        pass

    def refresh_access_token(self):
        pass

    async def save_tokens_to_db(self, db_engine):
        async with db_engine.acquire() as conn:
            await conn.execute(account.select())


if __name__ == '__main__':
    pass
    # token_manager = GoogleDriveTokenManager()