from token_data import TOKEN
from bot_handler import router
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import F
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section
)
from utils import programm_description

dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    '''Функция выводит сообщение при вызове команды /start и формиреут 2 кнопки вызова информации'''
    kb = [
        [
            types.KeyboardButton(text="Команды"),
            types.KeyboardButton(text="Описание бота"),
            types.KeyboardButton(text="Узнать больше о программе"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer_photo(photo=types.FSInputFile('assets/logo.jpg'))

    await message.answer('<b>Добро пожаловать в бот Московского Зоопарка</b>',  parse_mode="HTML")
    await message.answer("<u>Проект 'Возьмите животное под опеку'</u>",  parse_mode="HTML")
    await message.answer(f"Давайте выясним какое у вас тотемное животное", reply_markup=keyboard)



@dp.message(F.text.lower() == "команды")
async def commands(message: types.Message):
    '''Функция формирует описание основных команд при нажатии на кнопку "Команды"'''
    response = as_list(
        as_marked_section(
            Bold("Команды:"),
            "/lets_go - команда запускает викторину",
            "/stop - выход из викторины",
            "/more",
            marker="✅ ",
        ),
    )
    await message.answer(
        **response.as_kwargs()
    )


@dp.message(F.text.lower() == "описание бота")
async def description(message: types.Message):
    '''Функция формирует описание функциональности бота при нажатии на кнопку "Описание бота"'''
    await message.answer("Этот бот- викторина, помогающий вам подобрать животное для опеки")

@dp.message(F.text.lower() == "узнать больше о программе")
async def description(message: types.Message):
    '''Функция формирует описание программы московского зоопарка'''
    await message.answer_photo(photo=types.FSInputFile('assets/horse.jpg'))
    await message.answer(programm_description)

@dp.message(Command("more"))
async def description(message: types.Message):
    '''Функция формирует описание программы московского зоопарка'''
    await message.answer_photo(photo=types.FSInputFile('assets/horse.jpg'))
    await message.answer(programm_description)

@dp.message(Command("stop"))
async def description(message: types.Message):
    '''Функция формирует описание программы московского зоопарка'''
    pass

async def main() -> None:
    '''Функция формирует и запускает бота'''
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
