import aiohttp
import random
from utils import translate_recipe, curr_request, create_description
from token_data import url_list, url_filter
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types


router = Router()


class OrderRecipe(StatesGroup):
    waiting_for_category = State()
    waiting_for_recipes = State()


@router.message(Command("category_search_random"))
async def weather(message: Message, command: CommandObject, state: FSMContext):
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    await state.set_data({'rec_number': command.args})
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=url_list,
        ) as resp:
            data = await resp.json()
            builder = ReplyKeyboardBuilder()
            for date_item in data['meals']:
                builder.add(types.KeyboardButton(text=date_item.get('strCategory')))
            builder.adjust(4)
            await message.answer(
                f"Выберите категорию:",
                reply_markup=builder.as_markup(resize_keyboard=True),
            )
            await state.set_state(OrderRecipe.waiting_for_category.state)


@router.message(OrderRecipe.waiting_for_category)
async def recipe_by_category(message: types.Message, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=f'{url_filter}{message.text}',
        ) as resp:
            data = await resp.json()
            number_state = await state.get_data()
            data_shot = random.choices(data['meals'], k=int(number_state.get('rec_number', 3)))
            await state.set_data({'recipes': data_shot})
            builder = ReplyKeyboardBuilder()
            reipes_names = [translate_recipe(r.get('strMeal', '')).text.capitalize() for r in data_shot]
            builder.add(types.KeyboardButton(text='Покажи рецепты'))
            await message.answer(
                f"Как вам такие варианты: {', '.join(reipes_names)}",
                reply_markup=builder.as_markup(resize_keyboard=True),
            )
            await state.set_state(OrderRecipe.waiting_for_recipes.state)


@router.message(OrderRecipe.waiting_for_recipes)
async def recipe_by_category(message: types.Message, state: FSMContext):
    data = await state.get_data()
    recipes = await curr_request(data['recipes'])
    for rec in recipes:
        for meal in rec.get("meals"):
            answer = create_description(meal)
            await message.answer(answer)
