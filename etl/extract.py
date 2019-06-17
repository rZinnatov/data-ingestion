import io
import pandas as pd
import asyncio
import aiohttp
import async_timeout


class Extractor:
    def __init__(self, etlConfig):
        self.id = 0
        self.etlConfig = etlConfig
        self.proceedLoading = True

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._createTasks())
        loop.close()

    async def _createTasks(self):
        while self.proceedLoading:
            await asyncio.ensure_future(self._createTask())

    async def _createTask(self):
        with async_timeout.timeout(30):
            async with aiohttp.ClientSession() as session:
                async with session.get(self._buildUrl()) as response:
                    if response.status != 200:
                        # HACK:
                        # If status is not OK decide there is no more files to load (not good)
                        # TODO: use smarter way to handle status with retries
                        print(response.status)
                        self.proceedLoading = False
                        return

                    constent_bytes = await response.read()
                    self._handler(constent_bytes)

    def _buildUrl(self):
        # HACK:
        # every instance starts with id, then increments it by the number of instances
        # hence every instance do not process the same file twice
        url = f'{self.etlConfig.extractConfig.url}{self.etlConfig.extractConfig.id:012d}.csv'
        self.id += self.etlConfig.extractConfig.number_of_instances
        return url

    def _handler(self, content_bytes):
        df = pd.read_csv(io.BytesIO(content_bytes))
        df.dropna(inplace=True)

        df = self.etlConfig.transform(df, self.etlConfig.transformConfig)

        self.etlConfig.load(df, self.etlConfig.loadConfig)
