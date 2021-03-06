import asyncio
import logging


class DropboxFetcher:
    def __init__(self, interval=30, **kwargs):
        self.interval = interval

    async def run(self):
        while True:
            logging.info("fetcher for dropbox is working")
            await asyncio.sleep(self.interval)