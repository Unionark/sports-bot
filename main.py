import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from pattern_in_it import patterns

API_TOKEN = '8595642966:AAG4eVdxKpeISbuQIJzIG0EfweFeNB-V5Xg'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я спортивный бот. Чем могу помочь?")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
