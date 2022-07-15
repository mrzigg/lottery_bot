import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import db

async def user_exists(user_id):
    async with db.pool.acquire() as con:
        return await con.fetchval(''' SELECT id FROM tg_users WHERE id = $1 ''', user_id)
    
async def add_user(user_id, link):
    async with db.pool.acquire() as con:
        await con.execute(''' INSERT INTO tg_users (customer_id, bot_id, id, ref_tg_user_id) VALUES (1, 2061411546, $1, $2) ''', user_id, link)

async def find_link(user_id):
    async with db.pool.acquire() as con:
        return await con.fetchrow(''' SELECT * FROM tg_users WHERE id = $1 ''', user_id)

async def get_link(user_id):
    async with db.pool.acquire() as con:
        return await con.fetchval(''' SELECT ref_tg_user_id FROM tg_users WHERE id = $1 ''', user_id)

async def button_status(user_id):
    async with db.pool.acquire() as con:
        return await con.fetchval(''' SELECT button FROM tg_users WHERE id = $1 ''', user_id)

async def update_button(user_id, status):
    async with db.pool.acquire() as con:
        await con.execute(''' UPDATE tg_users SET button = $1 WHERE id = $2 ''', status, user_id)

async def update_gender(user_id, gender):
    async with db.pool.acquire() as con:
        await con.execute(''' UPDATE tg_users SET is_male = $1 WHERE id = $2 ''', gender, user_id)

async def update_age(user_id, age: str):
    async with db.pool.acquire() as con:
        await con.execute(''' UPDATE tg_users SET age_range = $1 WHERE id = $2 ''', age, user_id)

async def update_country(user_id, country: str):
    async with db.pool.acquire() as con:
        await con.execute(''' UPDATE tg_users SET country = $1 WHERE id = $2 ''', country, user_id)

async def all_users():
    async with db.pool.acquire() as con:
        return await con.fetch(''' SELECT id FROM tg_users ''')

async def get_button_status(user_id):
    async with db.pool.acquire() as con:
        return await con.fetchval(''' SELECT button_2 FROM tg_users WHERE id = $1 ''', user_id)

async def update_button_2(user_id):
    async with db.pool.acquire() as con:
        await con.execute(''' UPDATE tg_users SET button_2 = True WHERE id = $1 ''', user_id)