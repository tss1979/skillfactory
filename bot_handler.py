import random
from utils import animals, questions, build_answer, reserve_animal
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types

router = Router()
result = {}
animals = animals
questions_list = list(questions.keys())


class OrderQuize(StatesGroup):
    waiting_for_region = State()
    waiting_for_scape = State()
    waiting_for_do = State()
    waiting_for_character = State()
    waiting_for_spirit = State()
    waiting_for_food = State()
    waiting_for_picture = State()


@router.message(Command("lets_go"))
async def region(message: Message, state: FSMContext):
    await message.answer(f'<b><u>{questions_list[0]}</u></b>', parse_mode="HTML")
    builder = build_answer(questions_list[0])
    await message.answer(
        f"Выберите ответ:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(OrderQuize.waiting_for_region.state)


@router.message(OrderQuize.waiting_for_region)
async def landscape(message: types.Message, state: FSMContext):
    result['region'] = message.text.lower()
    await message.answer('Отлично! Следующий вопрос')
    await message.answer(f'<b><u>{questions_list[1]}</u></b>', parse_mode="HTML")
    builder = build_answer(questions_list[1])
    await message.answer(
        f"Выберите ответ:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(OrderQuize.waiting_for_scape.state)


@router.message(OrderQuize.waiting_for_scape)
async def to_do(message: types.Message, state: FSMContext):
    result['landscape'] = message.text.lower()
    await message.answer('Отлично! Следующий вопрос')
    await message.answer(f'<b><u>{questions_list[2]}</u></b>', parse_mode="HTML")
    builder = build_answer(questions_list[2])
    await message.answer(
        f"Выберите ответ:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(OrderQuize.waiting_for_do.state)


@router.message(OrderQuize.waiting_for_do)
async def character(message: types.Message, state: FSMContext):
    result.setdefault('n', 0)
    result['n'] += questions.get(questions_list[2]).index(message.text)
    await message.answer('Отлично! Следующий вопрос')
    await message.answer(f'<b><u>{questions_list[3]}</u></b>', parse_mode="HTML")
    builder = build_answer(questions_list[3])
    await message.answer(
        f"Выберите ответ:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(OrderQuize.waiting_for_character.state)


@router.message(OrderQuize.waiting_for_character)
async def spirit(message: types.Message, state: FSMContext):
    result['n'] += questions.get(questions_list[3]).index(message.text)
    await message.answer('Отлично! Следующий вопрос')
    await message.answer(f'<b><u>{questions_list[4]}</u></b>', parse_mode="HTML")
    builder = build_answer(questions_list[4])
    await message.answer(
        f"Выберите ответ:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(OrderQuize.waiting_for_spirit.state)


@router.message(OrderQuize.waiting_for_spirit)
async def food(message: types.Message, state: FSMContext):
    result['n'] += questions.get(questions_list[4]).index(message.text)
    await message.answer('Отлично! Следующий вопрос')
    await message.answer(f'<b><u>{questions_list[5]}</u></b>', parse_mode="HTML")
    builder = build_answer(questions_list[5])
    await message.answer(
        f"Выберите ответ:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(OrderQuize.waiting_for_food.state)


@router.message(OrderQuize.waiting_for_food)
async def picture(message: types.Message, state: FSMContext):
    result['food'] = message.text.lower()
    await message.answer('Отлично! Следующий вопрос')
    await message.answer(f'<b><u>{questions_list[6]}</u></b>', parse_mode="HTML")
    await message.answer_photo(photo=types.FSInputFile('assets/picture.png'))
    builder = build_answer(questions_list[6])
    await message.answer(
        f"Выберите ответ:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(OrderQuize.waiting_for_picture.state)

    @router.message(OrderQuize.waiting_for_picture)
    async def result_message(message: types.Message):
        result_animals = []
        result['n'] += questions.get(questions_list[6]).index(message.text)
        result['n'] = int(3 * result['n'] / 8)
        for animal, animL_list in animals.items():
            if all([result['region'] in animL_list, result['n'] in animL_list, \
                    result['landscape'] in animL_list, result['food'] in animL_list]):
                result_animals.append((animal, animL_list[-1]))
        if len(result_animals) == 0:
            totem_animal = reserve_animal
        else:
            totem_animal = random.choice(result_animals)
        animal, photo = totem_animal
        await message.answer('Поздравляю мы подобрали вам животное, о котором вы можете позаботиться')
        await message.answer(f'И это - {animal}')
        await message.answer_photo(photo=types.FSInputFile(photo))
