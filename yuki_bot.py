import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from yuki_personality import YukiPersonality
from aiohttp import web

# Безопасное получение токена
TOKEN = os.getenv("TOKEN", "8841854984:AAEp_xH6dM-eoeod9BNYZqyfNxkBowZ5wko")

bot = Bot(token=TOKEN)
dp = Dispatcher()
yuki = YukiPersonality(memory_file="yuki_memory_tg.json")


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Ядро Юки в Telegram запущено. Чего хочешь?")


@dp.message()
async def chat_handler(message: types.Message):
    text = (message.text or message.caption or "").lower()
    is_group = message.chat.type in ["group", "supergroup"]
    is_addressed = "юки" in text

    is_reply = False
    if message.reply_to_message:
        me = await bot.get_me()
        if message.reply_to_message.from_user.id == me.id:
            is_reply = True

    if is_group and not (is_addressed or is_reply):
        return

    yuki.autonomous_remember(message.text)
    msg = await message.answer("...")
    full_reply = ""

    for chunk in yuki.generate_ai_response_stream(message.text):
        full_reply += chunk
        if len(full_reply) % 20 == 0:
            await bot.edit_message_text(full_reply, chat_id=message.chat.id, message_id=msg.message_id)

    await bot.edit_message_text(full_reply, chat_id=message.chat.id, message_id=msg.message_id)


# Функция для веб-сервера (чтобы Render был доволен)
async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', lambda r: web.Response(text="Yuki is running!"))])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()


async def main():
    # Запускаем сервер
    await start_web_server()
    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())