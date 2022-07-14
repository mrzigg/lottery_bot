import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import db

async def lottery_exists():
    async with db.pool.acquire() as con:
        return await con.fetchrow(''' SELECT * FROM raffles ''')

async def photo_exists():
    async with db.pool.acquire() as con:
        return await con.fetchval(''' SELECT photo FROM raffles ''')

async def get_date():
    async with db.pool.acquire() as con:
        return await con.fetchval(''' SELECT end_timestamp FROM raffles ''')