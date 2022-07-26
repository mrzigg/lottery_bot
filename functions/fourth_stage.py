import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.raffle_progresses_db as progres_db

from config.load_all import bot


async def fourth_stage(user_id):
    info = await progres_db.get_function(user_id, "super_game_invites, super_game_to_invite")
    invites, to_invite = (info[0]+1), info[1]
    await progres_db.update_function(user_id, "super_game_invites", invites)
    
    if (to_invite-invites) == 1:
        text=f"<b>4 из 5 приглашений есть!</b>\nЭто почти победа!"
    elif (to_invite-invites) == 2:
        text=f"<b>3 из 5 приглашений есть!</b>\nУверенно идешь!"
    elif (to_invite-invites) == 3:
        text=f"<b>Второе приглашение есть)</b>\nОсталось еще <b>3.</b>"
    else:
        text=f"<b>Отлично, первое приглашение есть!</b>"
    
    return await bot.send_message(user_id, text)