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
        return await con.execute(''' INSERT INTO raffle_progresses (customer_id, bot_id, raffle_id, tg_user_id) VALUES ($1, $2, $3, $4) ''', customer_id, bot_id, raffle_id, user_id)

async def get_function(user_id, column): 
    async with db.pool.acquire() as con:
        return await con.fetchval(f''' SELECT {column} FROM raffle_progresses_extends WHERE customer_id = $1 AND bot_id = $2 AND raffle_id = $3 AND tg_user_id = $4 ''', customer_id, bot_id, raffle_id, user_id)

async def update_function(user_id, column, amount): 
    async with db.pool.acquire() as con:
        return await con.execute(f''' UPDATE raffle_progresses SET {column} = $1 WHERE customer_id = $2 AND bot_id = $3 AND raffle_id = $4 AND tg_user_id = $5 ''', amount, customer_id, bot_id, raffle_id, user_id)

async def get_row_function(user_id, column): 
    async with db.pool.acquire() as con:
        return await con.fetchrow(f''' SELECT {column} FROM raffle_progresses_extends WHERE customer_id = $1 AND bot_id = $2 AND raffle_id = $3 AND tg_user_id = $4 ''', customer_id, bot_id, raffle_id, user_id)

async def update_super_game(user_id, stage, invites): 
    async with db.pool.acquire() as con:
        return await con.execute(f''' UPDATE raffle_progresses SET super_game_stage = $1, super_game_invites = $2 WHERE customer_id = $3 AND bot_id = $4 AND raffle_id = $5 AND tg_user_id = $6 ''', stage, invites, customer_id, bot_id, raffle_id, user_id)