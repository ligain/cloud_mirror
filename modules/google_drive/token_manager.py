import json
from pathlib import Path

import httplib2

from core.settings import MissingConfigFile
from oauth2client import file, client, tools
import google_auth_httplib2


class GoogleDriveTokenManager:
    def __init__(self, credentials_file=None, scopes=None):
        self.credentials_file = Path(credentials_file)
        self.credentials = {}
        self.scopes = scopes

    def get_credentials_from_file(self):
        if not self.credentials_file.exists():
            raise MissingConfigFile(f"Credential file: {self.credentials_file} "
                                    "was not found")
        store = file.Storage('./token.json')
        flow = client.flow_from_clientsecrets(self.credentials_file,
                                              self.scopes,
                                              redirect_uri='http://localhost:8080/google-auth2-callback')
        self.credentials = tools.run_flow(flow, store)
        http = self.credentials.authorize(httplib2.Http())

    def get_tokens(self):
        pass

    def check_access_token(self):
        pass

    def refresh_access_token(self):
        pass

    async def save_tokens_to_db(self, engine):
        pass


if __name__ == '__main__':
    token_manager = GoogleDriveTokenManager()