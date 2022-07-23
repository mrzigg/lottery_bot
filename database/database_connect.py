import asyncpg

class Database:

    def __init__(self):
        self.pool = None

    async def create_pool(self):
        self.pool =  await asyncpg.create_pool(
                database="kwork_bot", 
                user='postgres', 
                password="horizonplay2017", 
                host="localhost", 
                port="5432",
                max_size=100
        )

    async def close(self):
        await self.pool.close()