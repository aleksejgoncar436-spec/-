import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yuki_personality import YukiPersonality

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

# 3. Обработка команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я Юки. Я готова к общению.")

# 4. Обработка всех текстовых сообщений
@dp.message(F.text)
async def handle_message(message: types.Message):
    try:
        # Показываем статус "печатает..."
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        # Генерация ответа через твой класс
        response = yuki.generate_ai_response(message.text)
        
        await message.answer(response)
    except Exception as e:
        logging.error(f"Ошибка при генерации ответа: {e}")
        await message.answer("Прости, у меня возникли технические неполадки.")

# 5. Главная функция запуска
async def main():
    # Очистка вебхуков — обязательно для решения конфликтов
    await bot.delete_webhook(drop_pending_updates=True)
    print("Юки успешно запущена и слушает сообщения!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
