from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import dp
from filters.during_sub import DuringSub2
from functions.message_routins import Routins
from buttons.check_subscription import callback_check_in


@dp.callback_query_handler(DuringSub2(), text='during_sub')
async def during_sub_check(call: types.CallbackQuery):
    await Routins.edit_callback(call=call)
    return await callback_check_in(callback_query=call)


@dp.callback_query_handler(text='during_sub_2')
async def during_sub_check(call: types.CallbackQuery):
    await call.answer()
    return await callback_check_in(callback_query=call)