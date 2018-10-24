from modules.google_drive.token_manager import GoogleDriveTokenManager


class GoogleDriveAPI:

    def __init__(self, token_manager=None):
        self.token_manager = token_manager
