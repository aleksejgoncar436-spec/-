import os
import asyncio
from aiogram import Bot, Dispatcher

# Вставь свой рабочий токен прямо СЮДА в кавычки для проверки
# БЕЗ пробелов и лишних символов
TOKEN = "8841854984:AAFBmLwKsdgs-Z5N5s5cbU3SBPRCDjHe2mU" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ... (остальной код бота)

async def main():
    if not TOKEN:
        print("Ошибка: Токен пустой!")
        return
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    print("Запуск polling...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
