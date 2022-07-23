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
        return await con.fetchval(''' INSERT INTO tickets (customer_id, bot_id, raffle_id, id, tg_user_id) VALUES ($1, $2, $3, NULL, $4) RETURNING id ''', customer_id, bot_id, raffle_id, user_id)

async def get_tickets(user_id):
    async with db.pool.acquire() as con:
        return await con.fetchval(''' SELECT COUNT(id) FROM tickets WHERE tg_user_id = $1 AND customer_id = $2 AND bot_id = $3 AND raffle_id = $4 ''', user_id, customer_id, bot_id, raffle_id)

async def all_tickets(user_id):
    async with db.pool.acquire() as con:
        return await con.fetch(''' SELECT id FROM tickets WHERE tg_user_id = $1 AND customer_id = $2 AND bot_id = $3 AND raffle_id = $4 ''', user_id, customer_id, bot_id, raffle_id)

async def last_ticket(user_id):
    async with db.pool.acquire() as con:
        return await con.fetchval(''' SELECT id FROM tickets WHERE tg_user_id = $1 AND customer_id = $2 AND bot_id = $3 AND raffle_id = $4 ORDER BY id DESC LIMIT 1 ''', user_id, customer_id, bot_id, raffle_id)

async def ten_tickets(user_id):
    async with db.pool.acquire() as con:
        return await con.fetch(''' 
        INSERT INTO tickets (customer_id, bot_id, raffle_id, id, tg_user_id) 
        VALUES 
        ($1, $2, $3, NULL, $4), ($1, $2, $3, NULL, $4), ($1, $2, $3, NULL, $4), ($1, $2, $3, NULL, $4), ($1, $2, $3, NULL, $4),
        ($1, $2, $3, NULL, $4), ($1, $2, $3, NULL, $4), ($1, $2, $3, NULL, $4), ($1, $2, $3, NULL, $4), ($1, $2, $3, NULL, $4)
        RETURNING id
        ''', customer_id, bot_id, raffle_id, user_id)