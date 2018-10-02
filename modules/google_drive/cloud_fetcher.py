import asyncio


class GoogleDriveFetcher:
    def __init__(self, interval=30, **kwargs):
        self.interval = interval

    async def run(self):
        while True:
            print("fetcher for google drive is working")
            await asyncio.sleep(self.interval)
