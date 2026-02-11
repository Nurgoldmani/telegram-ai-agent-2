import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = Groq(api_key=GROQ_API_KEY)


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Сәлем 👋 Привет!\n\n"
        "Мен қазақша және орысша сөйлей аламын.\n"
        "Я говорю на казахском и русском.\n\n"
        "Жазыңыз / Напишите что-нибудь 😊"
    )


@dp.message()
async def chat_handler(message: Message):
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты живой, дружелюбный ИИ ассистент. "
                        "Отвечай на языке пользователя (русский или казахский). "
                        "Если пользователь пишет на казахском — отвечай на казахском. "
                        "Если на русском — отвечай на русском. "
                        "Отвечай естественно, по-человечески, без официоза. "
                        "Не задавай слишком много лишних вопросов. "
                        "Не выдумывай имена. "
                        "Отвечай кратко, но по делу."
                    )
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ],
        )

        reply = completion.choices[0].message.content
        await message.answer(reply)

    except Exception as e:
        print("ERROR:", e)
        await message.answer("⚠ AI уақытша қолжетімсіз / временно недоступен.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
