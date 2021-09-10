"""
Functionality for working with Telegram
"""

import json

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())['tg']
    TG_TOKEN = sets['token']


bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


def keyboard(rows, inline=False):
    """ Make keyboard

    None                → No changes
    [] / [[]]           → Clear keyboard
    [x, y]              → Button column
    [[x, y], [z]]       → Button table
    [[{'data': 'x'}]]   → Inline buttons
    """

    # TODO: Check difference between [] / [[]] / types.ReplyKeyboardRemove()
    # TODO: easy way for inline mode, without parameter ` inline `

    # Type formation
    if isinstance(rows, (tuple, set)):
        rows = list(rows)
    elif not isinstance(rows, list):
        rows = [rows]

    # Empty queries

    if rows in ([], [[]]):
        if inline:
            return types.InlineKeyboardMarkup()

        return types.ReplyKeyboardRemove()

    if rows is None:
        return

    # Base
    if inline:
        buttons = types.InlineKeyboardMarkup()
    else:
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Inner elements formation
    if not isinstance(rows[0], (list, tuple)):
        rows = list(map(lambda cols: [cols], rows))

    # Filling
    for cols in rows:
        if not inline:
            buttons.add(*[types.KeyboardButton(col) for col in cols])
            continue

        buttons.add(
            *[
                types.InlineKeyboardButton(
                    col['name'],
                    **(
                        {'url': col['data']}
                        if col.get('type') == 'link'
                        else {'callback_data': col['data']}
                    ),
                ) for col in cols
            ]
        )

    return buttons

async def send(
    user, text='', buttons=None, inline=False, image=None, markup='Markdown',
):
    """ Send message """

    # TODO: users=[], forward=None, next_message=func
    # TODO: Если пустой buttons - убирать кнопки (но не None)
    # TODO: return bot.forward_message(user, forward, text)

    if not image:
        return await bot.send_message(
            user,
            text,
            reply_markup=keyboard(buttons, inline),
            parse_mode=markup,
            disable_web_page_preview=True,
        )

    return await bot.send_photo(
        user,
        image,
        text,
        reply_markup=keyboard(buttons, inline),
        parse_mode=markup,
    )
