import asyncio
import logging


class GoogleDriveFetcher:
    def __init__(self, interval=30, **kwargs):
        self.interval = interval

    async def run(self):
        while True:
            logging.info("fetcher for google drive is working")
            raise RuntimeError
            await asyncio.sleep(self.interval)
