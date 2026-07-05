import os
import asyncio
from aiogram import Bot, Dispatcher
from yuki_personality import YukiPersonality

# Читаем переменные из окружения
TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("8841854984:AAFBmLwKsdgs-Z5N5s5cbU3SBPRCDjHe2mU")

# Проверка, что переменные вообще есть
if not TOKEN or not GROQ_API_KEY:
    raise ValueError("Ошибка: TOKEN или GROQ_API_KEY не заданы в настройках!")

bot = Bot(token=TOKEN)
dp = Dispatcher()
yuki = YukiPersonality()

async def main():
    # Очистка очереди обновлений, чтобы бот не «давился» старыми сообщениями
    await bot.delete_webhook(drop_pending_updates=True)
    print("Юки проснулась и готова к работе...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
