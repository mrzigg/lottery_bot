from .main_data import customer_id, bot_id, raffle_id

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import db

async def add_user(user_id):
    async with db.pool.acquire() as con:
        await con.execute(''' INSERT INTO tickets (customer_id, bot_id, raffle_id, id, owner_tg_user_id) VALUES ($1, $2, $3, $4, $5) ''', customer_id, bot_id, raffle_id, user_id, user_id)

async def update_function(user_id, amount, column):
    async with db.pool.acquire() as con:
        await con.execute(f"UPDATE tickets SET {column} = $1 WHERE owner_tg_user_id = $2", amount, user_id)

async def get_tickets(user_id):
    async with db.pool.acquire() as con:
        return await con.fetchval(''' SELECT tickets FROM tickets WHERE owner_tg_user_id = $1 ''', user_id)

async def existing_link(user_id: int):
    async with db.pool.acquire() as con:
        return await con.fetchrow(''' SELECT * FROM tickets WHERE owner_tg_user_id = $1  ''', user_id)

async def update_invites(user_id: int, invites: int):
    async with db.pool.acquire() as con:
        await con.execute(''' UPDATE tickets SET invites = $1 WHERE owner_tg_user_id = $2 ''', invites, user_id)