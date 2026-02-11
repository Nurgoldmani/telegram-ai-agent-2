import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from openai import AsyncOpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Сәлем 👋 / Привет 👋\n\n"
        "Мен қазақша және орысша сөйлей аламын.\n"
        "Я могу общаться на казахском и русском.\n\n"
        "Напиши что-нибудь 🙂"
    )


@dp.message()
async def ai_handler(message: Message):
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты дружелюбный ИИ ассистент. "
                        "Отвечай на языке пользователя: если пишут на русском — отвечай на русском, "
                        "если на казахском — отвечай на казахском. "
                        "Пиши естественно, просто и по-человечески. "
                        "Не используй слишком официальные фразы. "
                        "Отвечай кратко и живо, как обычный человек."
                    )
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ]
        )

        answer = response.choices[0].message.content
        await message.answer(answer)

    except Exception as e:
        print(e)
        await message.answer("⚠️ AI уақытша қолжетімсіз / временно недоступен.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
