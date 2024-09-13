from aiogram import types, F, Router, Dispatcher
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# from aiogram.types import BufferedInputFile
# from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import valid_link, read_posts, chat
from models import User, Channel, SessionLocal

# from .keyboard import *
from keyboard import (
    start_keyboard,
    info_keyboard
)
# from admin import STATIC_DIR
from messages import (
    START_MESSAGE,
    INFO_MESSAGE,
    RUN_MESSAGE,
    TG_LINK_MESSAGE
)
# from main import bot

router = Router()
user_data = {}
# storage = MemoryStorage()
# dp = Dispatcher(storage=storage)


class Sequence(StatesGroup):
    enter_source = State()
    enter_time = State()
    enter_link = State()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    db = next(get_db())
    user = db.query(User).filter(User.user_name == user_id).first()
    if user:
        await message.answer('functions check', reply_markup=start_keyboard())
    else:
        new_user = User(user_name=user_id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user_data[message.from_user.id] = {"user_id": new_user.id}

        await message.answer(
            START_MESSAGE,
            reply_markup=start_keyboard()
        )


@router.callback_query(F.data == "info_func")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.edit_text(INFO_MESSAGE,
                                     reply_markup=info_keyboard())


@router.callback_query(F.data == "back_to_start_func")
async def go_back(callback: types.CallbackQuery):
    await callback.message.edit_text(START_MESSAGE,
                                     reply_markup=start_keyboard())


@router.callback_query(F.data == "start_func")
async def run_all(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.reply(RUN_MESSAGE)
    await state.set_state(Sequence.enter_source)


# @router.message(F.text)
@router.message(Sequence.enter_source)
async def run_message(message: types.Message, state: FSMContext):
    link = valid_link(message.text)
    print(link)
    if link:
        await message.bot.send_message(chat_id=message.chat.id,
                                       text=f'{TG_LINK_MESSAGE} {message.text}', parse_mode="HTML",
                                       disable_web_page_preview=True)
        text = await read_posts(link[5:])
        print(text)  # печатает последний пост из канала

        await state.set_state(Sequence.enter_time)
    else:
        await message.answer('Необходимо ввести сссылку на канал', parse_mode="HTML")


@router.message(Sequence.enter_time)
async def ask_for_time(message: types.Message, state: FSMContext):
    print('This is enter time, baby!')
    await message.answer("Введите дату начала перевода")
    print(message.text, 'я тут')
    await state.set_state(Sequence.enter_link)


@router.message(Sequence.enter_link)
async def ask_for_channel(message: types.Message, state: FSMContext):
    await message.answer("Введите ссылку на канал для публикации перевода")
    print(message.text, 'ой, нет, тут')
    await state.clear()
    # await Sequence.enter_link.set()
    print_channel = message.text
    db = next(get_db())
    eng_channel = Channel(likn=print_channel, user_id=1, type='eng_channel')
    db.add(eng_channel)
    db.commit()
    db.refresh(eng_channel)
    print('Готово')
# async def translate_text(message: types.Message):
#     chat_text = await chat(f'переведи на французский {text}')
#     await message.answer(chat_text, parse_mode="HTML")