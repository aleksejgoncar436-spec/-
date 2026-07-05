import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from yuki_personality import YukiPersonality

TOKEN = "8841854984:AAEp_xH6dM-eoeod9BNYZqyfNxkBowZ5wko"

bot = Bot(token=TOKEN)
dp = Dispatcher()
yuki = YukiPersonality(memory_file="yuki_memory_tg.json")


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Ядро Юки в Telegram запущено. Чего хочешь?")


# ОДИН единственный обработчик для всех сообщений
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

    # Фильтр: если группа и не обратились — выходим
    if is_group and not (is_addressed or is_reply):
        return

    # Если дошли сюда, Юки отвечает
    yuki.autonomous_remember(message.text)

    msg = await message.answer("...")
    full_reply = ""

    for chunk in yuki.generate_ai_response_stream(message.text):
        full_reply += chunk
        if len(full_reply) % 20 == 0:
            await bot.edit_message_text(full_reply, chat_id=message.chat.id, message_id=msg.message_id)

    await bot.edit_message_text(full_reply, chat_id=message.chat.id, message_id=msg.message_id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())