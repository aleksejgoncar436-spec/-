import os
import asyncio
from aiogram import Bot, Dispatcher
from yuki_personality import YukiPersonality

# Берем токен строго из Render
TOKEN = os.getenv("8841854984:AAFBmLwKsdgs-Z5N5s5cbU3SBPRCDjHe2mU")

bot = Bot(token=TOKEN)
dp = Dispatcher()
yuki = YukiPersonality()

# ... здесь твои хендлеры ...

async def main():
    # Эта команда ОЧИЩАЕТ все старые очереди, которые вызывали конфликт
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот успешно запущен и готов к работе.")
    await dp.start_polling(bot)

@dp.message()
async def echo(message: types.Message):
    print(f"Получено сообщение: {message.text}") # Это должно появиться в логах Render!
    await message.answer("Я получила твоё сообщение!"

if __name__ == "__main__":
    asyncio.run(main())
