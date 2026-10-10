import asyncio
import random
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from urllib.parse import quote
API_TOKEN = ''
WEATHER_API_KEY = ''
NEWS_API_TOKEN = ''
COUNTRY_CODES = {
    "оаэ": "ae", "объединенные арабские эмираты": "ae",
    "аргентина": "ar", "австрия": "at", "австралия": "au",
    "бельгия": "be", "болгария": "bg", "бразилия": "br",
    "канада": "ca", "швейцария": "ch", "китай": "cn",
    "колумбия": "co", "куба": "cu", "чехия": "cz",
    "германия": "de", "египет": "eg", "франция": "fr",
    "великобритания": "gb", "соединенное королевство": "gb",
    "греция": "gr", "гонконг": "hk", "венгрия": "hu",
    "индонезия": "id", "ирландия": "ie", "израиль": "il",
    "индия": "in", "италия": "it", "япония": "jp",
    "южная корея": "kr", "республика корея": "kr",
    "литва": "lt", "латвия": "lv", "марокко": "ma",
    "мексика": "mx", "малайзия": "my", "нигерия": "ng",
    "нидерланды": "nl", "голландия": "nl", "норвегия": "no",
    "новая зеландия": "nz", "филиппины": "ph", "польша": "pl",
    "португалия": "pt", "румыния": "ro", "сербия": "rs",
    "россия": "ru", "российская федерация": "ru",
    "саудовская аравия": "sa", "швеция": "se", "сингапур": "sg",
    "словения": "si", "словакия": "sk", "таиланд": "th",
    "турция": "tr", "тайвань": "tw", "украина": "ua",
    "сша": "us", "соединенные штаты": "us",
    "соединенные штаты америки": "us", "венесуэла": "ve",
    "юар": "za", "южно-африканская республика": "za",
}
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
class WeatherStates(StatesGroup):
    waiting_for_city = State()
    waiting_for_coutnry = State() 
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! я бот,который может помочь тебе с различными задачами напиши /help чтобы узнать что я могу")
@dp.message(Command("help"))
async def help(message: types.Message):
    await message.answer("Я могу помочь тебе с различными задачами, например:\n"
                         "/start - начать работу с ботом\n"
                         "/info - получить информацию о боте\n"
                         "/weather - узнать погоду\n"
                         "/news - узнать последние новости\n"
                         "/joke - случайная шутка\n"
                         "/roll - бросить кубик\n"
                         "/choose - выбрать вариант из списка\n"
                         "/fun - получить случайную фишку\n")

FUN_FACTS = [
    "💡 Полезный факт: чтобы быстро принять решение, попробуйте думать не о вариантах, а о последствии, которое вам ближе.",
    "🎯 Фишка: сделайте 1 маленькое действие прямо сейчас — и momentum начнёт работать на вас.",
    "🌟 Совет: если день скучный, добавьте одну необычную привычку — и уже всё выглядит иначе.",
    "🧠 Интересный момент: короткие задачи лучше делать сразу, чем откладывать их в длинный список дел.",
    "✨ Удача чаще любит тех, кто делает шаги, а не ждёт идеального момента.",
]

@dp.message(Command("fun"))
async def fun(message: types.Message):
    fact = random.choice(FUN_FACTS)
    await message.answer(fact)

@dp.message(Command("joke"))
async def joke(message: types.Message):
    jokes = [
        "Почему программист не боится темноты? Потому что он всегда пишет код в светлом режиме.",
        "Что сказал компьютер, когда его попросили отдохнуть? 'Я в отпуске, но память всё ещё работает.'",
        "Почему разработчик любит кофе? Потому что без него даже отладка кажется веселой.",
        "Я хотел стать продуктивным, но вместо этого открыл 15 вкладок и стал философом.",
        "Если работа не идёт, значит, пора сделать паузу — иногда даже код любит отдых.",
    ]
    await message.answer(random.choice(jokes))

@dp.message(Command("roll"))
async def roll(message: types.Message):
    dice = random.randint(1, 6)
    await message.answer(f"🎲 Бросок кубика: {dice}")

@dp.message(Command("choose"))
async def choose(message: types.Message):
    text = (message.get_args() or "").strip()
    if not text:
        await message.answer("Используй формат: /choose вариант1 | вариант2 | вариант3")
        return

    options = [part.strip() for part in text.split("|") if part.strip()]
    if len(options) < 2:
        await message.answer("Нужно минимум 2 варианта, например: /choose кофе | чай | сок")
        return

    winner = random.choice(options)
    await message.answer(f"🎯 Я выбираю: {winner}")

@dp.message(Command("info"))
async def info(message: types.Message):        
    await message.answer("Я бот, который может помочь тебе с различными задачами. Моя цель - сделать твою жизнь проще и удобнее.")
"""НОВОСТИ"""
@dp.message(Command("news"))
async def news(message: types.Message, state: FSMContext):
    await message.answer("Введите название страны по-русски, например США или Германия")
    await state.set_state(WeatherStates.waiting_for_coutnry)
@dp.message (WeatherStates.waiting_for_coutnry)    
async def process_coutry(message: types.Message, state: FSMContext):
    country = (message.text or "").strip().casefold().replace("ё", "е")
    country_code = COUNTRY_CODES.get(country)
    if country_code is None:
        await message.answer("Не удалось распознать страну. Попробуйте, например:  США или Германия.")
        await state.clear()
        return
    await message.answer(f"Ищу новости для страны: {country}")
    news_report = await get_news(country_code)
    await message.answer(news_report)
    await state.clear()
async def get_news(country_name : str):
    url = "https://newsapi.org/v2/top-headlines"
    payload = {
        "country": country_name,
        "apiKey": NEWS_API_TOKEN,
        "pageSize": 3
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=payload) as response:
            data = await response.json()
            if response.status == 200:
                articles = data.get("articles", [])
                if not articles:
                    return "В этой стране сейчас нет свежих новостей."
                report = "Последние новости:\n\n"
                for article in articles:
                    title = article.get("title", "Без заголовка")
                    link = article.get("url", "")
                    report += f"🔹 {title}\n🔗 Читать: {link}\n\n"
                return report
            return "Извини, не удалось найти новости для этой страны. Проверь код страны."
    
#Погода
@dp.message(Command("weather"))
async def weather(message: types.Message, state: FSMContext):
    await message.answer("Введите названия города,чтобы узнать погоду")
    await state.set_state(WeatherStates.waiting_for_city)
@dp.message(WeatherStates.waiting_for_city)
async def process_city(message: types.Message, state: FSMContext):
    city = message.text
    weather_report = await get_weather(city)
    await message.answer(f"Ищу погоду для города: {city}")
    await message.answer(weather_report)
    await state.clear()
async def get_weather(city_name: str):
    # Строго правильный URL без лишних букв f и знаков вопросов
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    payload = {
        "q": city_name,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=payload) as response:
            if response.status == 200:
                data = await response.json()
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                
                return f"Погода в городе {city_name}:\nГрадусы: {temp}°C\nНа улице: {desc}"
            else:
                return "Извини, не удалось найти такой город. Проверь название."
            
async def main():
    print("Бот успешно запущен и слушает сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())