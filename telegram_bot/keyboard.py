from aiogram import types


def start_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Инструкция",
                                       callback_data="info_func"),
            types.InlineKeyboardButton(text="Начать",
                                       callback_data="start_func")
        ],
        # [types.InlineKeyboardButton(text="Подтвердить",
        #                             callback_data="num_finish")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def info_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Назад",
                                       callback_data="back_to_start_func"),
            types.InlineKeyboardButton(text="Начать",
                                       callback_data="start_func")
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# def run_keyboard():
#     buttons = [
#         [
#             types.InlineKeyboardButton(text="Назад",
#                                        callback_data="back_func"),
#             # types.InlineKeyboardButton(text="Начать",
#             #                            callback_data="start_func")
#         ],
#     ]
#     keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
#     return keyboard
