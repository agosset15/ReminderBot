from datetime import datetime, timedelta
from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .config import bot, Ad
from db.methods.get import get_remind, get_user_by_telegram_id
from db.methods.create import create_user, create_remind
from db.methods.delete import delete_remind

router = Router()

main_td = '%H-%M %d.%m.%Y'


async def sendadd():
    tm = datetime.now().strftime(main_td)
    rem = get_remind(tm)
    for i in rem:
        await bot.send_message(i.user, i.text)
        delete_remind(i.id)


@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    usr = get_user_by_telegram_id(message.from_user.id)
    code = extract_unique_code(message.text)
    if usr is not None:
        await message.answer('Напишите напоминание')
        await state.set_state(Ad.text)
    else:
        create_user(message.from_user.id, message.from_user.full_name, message.from_user.username, code)
        await message.answer('Напишите напоминание')
        await state.set_state(Ad.text)


@router.message(Ad.text)
async def add_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(f"Напишите когда хотите получить это напоминание"
                         f"\n\nФормат: {html.code('ЧАСЫ-МИНУТЫ ДЕНЬ.МЕСЯЦ.ГОД')}", parse_mode='HTML',
                         reply_markup=keyboard())
    await state.set_state(Ad.timedate)


@router.message(Ad.timedate)
async def add_timedate(message: Message, state: FSMContext):
    try:
        dt = datetime.strptime(message.text, main_td)
        text = await state.get_data()
        text = text['text']
        await message.answer(f"Отлично.\n\n{text}\nВ {message.text}"
                             f"\nПодтверждаете? Напишите что угодно в ответ, если согласны, или /start")
        await state.update_data(timedate=message.text)
        await state.set_state(Ad.conf)
    except ValueError:
        await message.answer(f"Вы ввели дату и время в неправильном формате"
                             f"\n\nПример: {html.code('23-59 31.12.2023')}", parse_mode='HTML')


@router.callback_query(Ad.timedate)
async def call_timedate(call: CallbackQuery, state: FSMContext):
    time = int(call.data.split('_')[0])
    will = datetime.now() + timedelta(hours=time)
    will = will.strftime(main_td)
    text = await state.get_data()
    text = text['text']
    await call.message.answer(f"Отлично.\n\n{text}\nВ {will}"
                              f"\nПодтверждаете? Напишите что угодно в ответ, если согласны, или /start")
    await state.update_data(timedate=will)
    await state.set_state(Ad.conf)


@router.message(Ad.conf)
async def add_conf(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    create_remind(message.from_user.id, data['timedate'], data['text'])
    await message.answer('Done!')


def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None


def keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="2 часа", callback_data='2_hours')
    kb.button(text="3 часа", callback_data='3_hours')
    kb.button(text="6 часов", callback_data='6_hours')
    kb.button(text="12 часов", callback_data='12_hours')
    kb.button(text="24 часов", callback_data='24_hours')
    return kb.as_markup()
