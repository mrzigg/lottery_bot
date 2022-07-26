from .main_data import customer_id, bot_id, raffle_id

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import db


async def lottery_exists():
    async with db.pool.acquire() as con:
        return await con.fetchrow(''' SELECT * FROM raffles WHERE customer_id = $1 AND bot_id = $2 AND id = $3 ''', customer_id, bot_id, raffle_id)

async def get_date():
    async with db.pool.acquire() as con:
        return await con.fetchval(''' SELECT end_timestamp FROM raffles WHERE customer_id = $1 AND bot_id = $2 AND id = $3 ''', customer_id, bot_id, raffle_id)

async def prizes():
    async with db.pool.acquire() as con:
        return await con.fetchval(''' SELECT prizes FROM raffles WHERE customer_id = $1 AND bot_id = $2 ''', customer_id, bot_id)