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

    async def fake_send_message(group_id, text):
        sent.append((group_id, text))

    monkeypatch.setattr(bot.client, 'send_message', fake_send_message)

    sleeps = []

    async def fake_sleep(seconds):
        sleeps.append(seconds)

    monkeypatch.setattr(bot.asyncio, 'sleep', fake_sleep)

    monkeypatch.setattr(bot, 'MESSAGES', [f"q{i}" for i in range(150)])
    monkeypatch.setattr(bot, 'REPLIES', [f"a{i}" for i in range(150)])
    monkeypatch.setattr(bot, 'USERNAMES', ['user1', 'user2'])

    def fake_choice(seq):
        return seq[0]

    monkeypatch.setattr(bot.random, 'choice', fake_choice)

    await bot.post_pairs()

    assert len(sent) == 200
    assert sleeps == [15] * 100
    for i in range(0, len(sent), 2):
        q_idx = i // 2
        assert sent[i] == (1, f"user1 q{q_idx}")
        assert sent[i + 1] == (1, f"user2 a{q_idx}")

@pytest.mark.asyncio
async def test_daily_scheduler_waits_until_midnight(monkeypatch, bot_module):
    bot = bot_module

    async def fake_post_pairs():
        pass
    monkeypatch.setattr(bot, 'post_pairs', fake_post_pairs)

    original_datetime = bot.datetime

    class FixedDatetime(original_datetime):
        @classmethod
        def now(cls, tz=None):
            return original_datetime(2023, 1, 1, 23, 30)

    monkeypatch.setattr(bot, 'datetime', FixedDatetime)

    sleeps = []

    async def fake_sleep(seconds):
        sleeps.append(seconds)
        raise asyncio.CancelledError()

    monkeypatch.setattr(bot.asyncio, 'sleep', fake_sleep)

    with pytest.raises(asyncio.CancelledError):
        await bot.daily_scheduler()

    assert sleeps == [30 * 60]


def test_validate_lists_mismatch(monkeypatch, bot_module):
    bot = bot_module
    monkeypatch.setattr(bot, 'MESSAGES', ['a', 'b'])
    monkeypatch.setattr(bot, 'REPLIES', ['a'])
    with pytest.raises(ValueError):
        bot.validate_lists()


def test_validate_lists_empty(monkeypatch, bot_module):
    bot = bot_module
    monkeypatch.setattr(bot, 'MESSAGES', [])
    monkeypatch.setattr(bot, 'REPLIES', [])
    with pytest.raises(ValueError):
        bot.validate_lists()

