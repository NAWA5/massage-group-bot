# Massage Group Bot

This is a Telegram bot designed to manage and automate group messages. The bot can:
- Send automated welcome messages
- Respond to specific keywords
- Log group activity
- Support multi-session accounts

## Features
- Multiple account support via Telethon
- Import users from Excel
- Reply automation
- Group monitoring

## Requirements
- Python 3.8+
- Telethon
- pandas
- openpyxl

## Setup

1. Clone the repository:
```bash
git clone https://github.com/NAWA5/massage-group-bot.git
```

2. Install the dependencies:
```bash
pip install -r requirements.txt
```

3. Configure `.env` for your API credentials and settings. An example file
   named `.env.example` is provided. Copy it and fill in your values:

   ```bash
   cp .env.example .env
   ```

   The bot requires the following variables:

   | Name      | Description                        |
   |-----------|------------------------------------|
   | `API_ID`  | Telegram API ID                    |
   | `API_HASH`| Telegram API hash                  |
   | `BOT_TOKEN` | Token of the bot obtained from BotFather |
   | `GROUP_ID` | Numeric ID of the group the bot should post in |

   Make sure `.env` is in the project root.

4. Run the bot:
   ```bash
   python bot.py
   ```

   `messages.txt` and `replies.txt` must also be located in the project root.

## How it works

`bot.py` uses Telethon to send messages to the chat specified by
`GROUP_ID`. During each run it performs the following loop:

1. Randomly select a username from `usernames.txt`.
2. Send one question from `messages.txt` and one answer from `replies.txt`.
3. Repeat until 100 pairs have been sent.
4. Sleep until midnight and start over.

The bot therefore sends 100 question/answer pairs every day at roughly
the same time.

## Troubleshooting

- Ensure the bot token and group ID in `.env` are correct.
- Add the bot to your Telegram group with permission to send messages.
- Check that `messages.txt`, `replies.txt` and `usernames.txt` exist and
  contain content.

### Expected behaviour

Once started, the bot will post pairs of messages in the configured
group. Each pair is separated by 15 seconds. After all 100 pairs are
sent the bot idles until the next day and then repeats.

## Author
Developed by NAWA5
