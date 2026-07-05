import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from yuki_personality import YukiPersonality

TOKEN = "8841854984:AAEtca0oFoPzYE8TkQRdaVJevA5n0izL-XA"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ИСПРАВЛЕННАЯ СТРОКА:
yuki = YukiPersonality()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Ядро Юки активировано. Я с тобой.")

@dp.message()
async def chat_handler(message: types.Message):
    if not message.text: return
    
    msg = await message.answer("...")
    full_reply = ""

    for chunk in yuki.generate_ai_response_stream(message.text):
        full_reply += chunk
        if len(full_reply) % 20 == 0:
            await bot.edit_message_text(full_reply, chat_id=message.chat.id, message_id=msg.message_id)

    if not full_reply.strip():
        full_reply = "..."
    
    await bot.edit_message_text(full_reply, chat_id=message.chat.id, message_id=msg.message_id)

async def main():
    # Удаляем все старые вебхуки и сбрасываем зависшие обновления
    # Это ключевая строка для решения TelegramConflictError
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("Сессия очищена. Запуск бота...")
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
