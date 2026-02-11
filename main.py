import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from groq import Groq

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not found!")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = Groq(api_key=GROQ_API_KEY)

@dp.message()
async def chat_with_ai(message: Message):
    user_text = message.text

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a powerful AI Telegram assistant."},
                {"role": "user", "content": user_text}
