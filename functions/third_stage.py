import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import bot
import database.raffle_progresses_db as progres_db

from config.bot_name import link
            

async def third_stage(user_id):
    info = await progres_db.get_row_function(user_id, "super_game_invites, super_game_to_invite, super_game_duration")
    invites, to_invite, duration = (info[0]+1), info[1], info[2]
    await progres_db.update_function(user_id, "super_game_invites", invites)

    if (to_invite-invites) == 1:
        text=f"<b>Отлично!</b>\n\n<b>1 из {to_invite}</b> приглашений есть.\nОсталось совсем чуть-чуть 😅"
    elif (to_invite-invites) == 2:
        text=f"<b>+1 друг принял приглашение!</b> 😊\n\nОсталось пригласить <b>2</b> друзей)\n\nСкорее всего... В этом пари ты заберешь победу)" 
    elif (to_invite-invites) == 3:
        text=f"<b>Твой друг принял участие в розыгрыше!</b>☺️\nЧтобы забрать выигрыш - тебе осталось пригласить <b>3</b> друзей)"
    elif (to_invite-invites) == 4:
        text=f"<b>Еще +1 есть!</b>\nОсталось пригласить <b>4</b> друзей)\nУверенно идешь))"
    elif (to_invite-invites) == 5:
        text=f"<b>+1 приглашение есть! 😁</b>\nЧтобы забрать выигрыш - тебе осталось пригласить <b>5</b> друзей)"
    elif (to_invite-invites) == 6:
        text=f"<b>Воу, еще +1! </b>\nОсталось пригласить  еще <b> 6 </b> друзей)\nНа кону <b>{duration*40}</b> лотерейных билетов!\nКак думаешь, успеешь?"
    elif (to_invite-invites) == 7:
        text=f"<b>+1 приглашение принято!</b> 🥳\nОсталось еще <b>7 друзей.</b>"
    elif (to_invite-invites) == 8:
        text=f"<b>Еще +1 есть)</b>\nОсталось пригласить <b>8</b> друзей)\nХороший старт!"
    elif (to_invite-invites) > 8:
        text=f"<b>Твой +1 друг в теме</b>\nОсталось еще <b>{to_invite-invites}</b> друзей добавить)\nНа кону <b>{duration*40}</b> лотерейных билетов!"
        
    return await bot.send_message(user_id, text+f"\n\nСсылка для приглашений:\n{link}{user_id}", disable_web_page_preview=True)