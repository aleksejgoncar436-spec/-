import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yuki_personality import YukiPersonality

# Настройка логирования (поможет видеть, что бот делает)
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("8841854984:AAFBmLwKsdgs-Z5N5s5cbU3SBPRCDjHe2mU")

# Добавь этот блок для отладки
if TOKEN is None:
    print("КРИТИЧЕСКАЯ ОШИБКА: Переменная окружения 'TOKEN' не найдена!")
    exit(1) # Завершаем программу, чтобы не было ошибки Aiogram
else:
    print(f"Токен успешно считан, длина: {len(TOKEN)}")

bot = Bot(token=TOKEN)

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я Юки, твой AI-помощник.")

# Обработчик любого текстового сообщения
@dp.message(F.text)
async def text_handler(message: types.Message):
    print(f"Получено сообщение: {message.text}") # Это должно быть в логах Render
    
    # Отправляем "статус печати", чтобы пользователь видел, что бот работает
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    response = yuki.generate_ai_response(message.text) # Убедись, что имя метода верное
    await message.answer(response)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
