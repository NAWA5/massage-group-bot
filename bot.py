import asyncio
import os
import random
from datetime import datetime, timedelta

from dotenv import load_dotenv
from telethon import TelegramClient


load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

if not all([API_ID, API_HASH, BOT_TOKEN, GROUP_ID]):
    raise RuntimeError(
        "API_ID, API_HASH, BOT_TOKEN, and GROUP_ID must be set in the .env file"
    )

client = TelegramClient('bot', int(API_ID), API_HASH)


def load_list(filename: str) -> list[str]:
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


MESSAGES = load_list("messages.txt")
REPLIES = load_list("replies.txt")
USERNAMES = load_list("usernames.txt")


async def post_pairs():
    """Send 100 question/answer pairs with a 15-second delay."""
    for _ in range(100):
        username = random.choice(USERNAMES)
        question = random.choice(MESSAGES)
        answer = random.choice(REPLIES)

        await client.send_message(int(GROUP_ID), f"{username} {question}")
        await client.send_message(int(GROUP_ID), f"{username} {answer}")
        await asyncio.sleep(15)


async def daily_scheduler():
    while True:
        await post_pairs()
        now = datetime.now()
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        await asyncio.sleep((tomorrow - now).total_seconds())


def main():
    client.start(bot_token=BOT_TOKEN)
    with client:
        client.loop.run_until_complete(daily_scheduler())


if __name__ == "__main__":
    main()
