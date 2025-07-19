import importlib
import asyncio
import types
import pytest

# Fixture to ensure environment variables are set before importing bot
@pytest.fixture
def bot_module(monkeypatch):
    monkeypatch.setenv('API_ID', '1')
    monkeypatch.setenv('API_HASH', 'hash')
    monkeypatch.setenv('BOT_TOKEN', 'token')
    monkeypatch.setenv('GROUP_ID', '1')
    import bot
    return importlib.reload(bot)


def test_loads_message_and_reply_lists(bot_module):
    bot = bot_module
    with open('messages.txt', encoding='utf-8') as f:
        messages = [line.strip() for line in f if line.strip()]
    with open('replies.txt', encoding='utf-8') as f:
        replies = [line.strip() for line in f if line.strip()]
    assert bot.MESSAGES == messages
    assert bot.REPLIES == replies


@pytest.mark.asyncio
async def test_post_pairs_scheduling(monkeypatch, bot_module):
    bot = bot_module

    sent = []

    class DummyClient:
        async def send_message(self, group_id, message):
            sent.append((group_id, message))

    monkeypatch.setattr(bot, 'client', DummyClient())

    sleeps = []

    async def fake_sleep(seconds):
        sleeps.append(seconds)

    monkeypatch.setattr(bot.asyncio, 'sleep', fake_sleep)

    monkeypatch.setattr(bot, 'MESSAGES', ['q'])
    monkeypatch.setattr(bot, 'REPLIES', ['a'])
    monkeypatch.setattr(bot, 'USERNAMES', ['user'])

    await bot.post_pairs()

    assert len(sent) == 200
    assert sleeps == [15] * 100
