import asyncio
import logging
import os
import random
from datetime import datetime, timedelta

from dotenv import load_dotenv
from telethon import TelegramClient


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


def validate_lists():
    """Ensure message and reply lists have equal non-zero length."""
    if not MESSAGES or not REPLIES:
        logger.error("messages.txt or replies.txt is empty")
        raise ValueError("messages.txt and replies.txt must not be empty")
    if len(MESSAGES) != len(REPLIES):
        logger.error(
            "messages.txt has %d lines but replies.txt has %d",
            len(MESSAGES),
            len(REPLIES),
        )
        raise ValueError(
            "messages.txt and replies.txt must contain the same number of lines"
        )


async def post_pairs():
    """Send matching question/reply pairs with a delay between them."""
    for i, (question, answer) in enumerate(zip(MESSAGES, REPLIES)):
        if i >= 100:
            break

        question_user = random.choice(USERNAMES)
        if len(USERNAMES) > 1:
            answer_user = random.choice([u for u in USERNAMES if u != question_user])
        else:
            answer_user = question_user

        logger.info("Sending question %d: %s", i, question)
        await client.send_message(int(GROUP_ID), f"{question_user} {question}")
        # Delay so the reply doesn't immediately follow the question
        await asyncio.sleep(15)
        logger.info("Sending reply %d: %s", i, answer)
        await client.send_message(int(GROUP_ID), f"{answer_user} {answer}")


async def daily_scheduler():
    logger.info("Scheduler starting")
    validate_lists()
    while True:
        await post_pairs()
        now = datetime.now()
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        sleep_time = (tomorrow - now).total_seconds()
        logger.info("Sleeping %.0f seconds until midnight", sleep_time)
        await asyncio.sleep(sleep_time)


def main():
    client.start(bot_token=BOT_TOKEN)
    with client:
        client.loop.run_until_complete(daily_scheduler())


if __name__ == "__main__":
    main()

