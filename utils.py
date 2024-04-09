from googletrans import Translator
import aiohttp
import asyncio

translator = Translator()


def translate_recipe(recipe):
    '''Функция переводит поданную в качестве аргумента строку на русский язык'''
    return translator.translate(recipe, dest='ru')


async def fetch(session, url):
    async with session.get(url) as resp:
        '''Функция делает запрос сессию и возвращает ответ с API'''
        return await resp.json()


async def curr_request(data: list):
    async with aiohttp.ClientSession() as session:
        '''Функция запускает сессию и формирует список асинхронных функций для запроса'''
        urls = [f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={x.get("idMeal")}' for x in data]
        fetch_awaitables = [
            fetch(session, url)
            for url in urls
        ]
        return await asyncio.gather(*fetch_awaitables)


def create_description(meal):
    ingredients = []
    answer = f'{translate_recipe(meal.get("strMeal")).text}\n\nРецепт:\n'
    answer += translate_recipe(meal.get('strInstructions')).text + '\n' + '\n'
    for key in meal.keys():
        if 'strIngredient' in key and meal.get(key) != '' and meal.get(key) is not None:
            ingredients.append(translate_recipe(meal.get(key)).text)
    answer += f'Ингредиенты: {", ".join(ingredients)}'
    return answer
