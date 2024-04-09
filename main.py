from token_data import TOKEN
from recipes_handler import router
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section
)

dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    '''Функция выводит сообщение при вызове команды /start и формиреут 2 кнопки вызова информации'''
    kb = [
        [
            types.KeyboardButton(text="Команды"),
            types.KeyboardButton(text="Описание бота"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    await message.answer(f"Привет! С чего начнем?", reply_markup=keyboard)


@dp.message(F.text.lower() == "команды")
async def commands(message: types.Message):
    '''Функция формирует описание основных команд при нажатии на кнопку "Команды"'''
    response = as_list(
        as_marked_section(
            Bold("Команды:"),
            "/category_search_random 3 - команда вызова категорий и цифрой задается количество рецептов",
            "кнопка категории - выбор рецептов из категории",
            "кнопка показать рецепты - показать рецепты из показанного предложения",
            marker="✅ ",
        ),
    )
    await message.answer(
        **response.as_kwargs()
    )


@dp.message(F.text.lower() == "описание бота")
async def description(message: types.Message):
    '''Функция формирует описание функциональности бота при нажатии на кнопку "Описание бота"'''
    await message.answer("Этот бот предоставляет информацию рецептах по заданной категории")


async def main() -> None:
    '''Функция формирует и запускает бота'''
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
