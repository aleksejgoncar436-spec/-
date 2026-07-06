import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yuki_personality import YukiPersonality
from aiohttp import web

# 1. Настройка логирования (чтобы видеть в Render, что происходит)
logging.basicConfig(level=logging.INFO)

# 2. Получение переменных окружения
TOKEN = os.getenv("8841854984:AAFBmLwKsdgs-Z5N5s5cbU3SBPRCDjHe2mU")
GROQ_API_KEY = os.getenv("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")

# Проверка, чтобы бот сразу сказал, чего ему не хватает
# ВРЕМЕННО: Вставь свой токен прямо сюда (только для теста!)
TOKEN = "8841854984:AAFBmLwKsdgs-Z5N5s5cbU3SBPRCDjHe2mU"
GROQ_API_KEY = "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"

# Инициализация
bot = Bot(token=TOKEN)
dp = Dispatcher()
yuki = YukiPersonality()

async def handle(request):
    return web.Response(text="Юки онлайн!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
port = int(os.getenv("PORT", 10000))
site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# 3. Обработка команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я Юки. Я готова к общению.")

# 4. Обработка всех текстовых сообщений
@dp.message(F.text)
async def handle_message(message: types.Message):
    try:
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        full_response = ""
        # Собираем ответ из генератора
        for chunk in yuki.generate_ai_response(message.text):
            full_response += chunk
        
        # Если вдруг генератор ничего не вернул
        if not full_response:
            full_response = "Юки сейчас немного задумалась..."
            
        await message.answer(full_response)
        
    except Exception as e:
        logging.error(f"Ошибка при генерации ответа: {e}")
        await message.answer("Прости, у меня возникли технические неполадки.")

# 5. Главная функция запуска
async def main():
    # ЗАПУСКАЕМ ВЕБ-СЕРВЕР ОБЯЗАТЕЛЬНО
    await start_web_server()
    
    await bot.delete_webhook(drop_pending_updates=True)
    print("Юки успешно запущена и слушает сообщения!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Именно так запускается современный aiogram
    asyncio.run(main())
