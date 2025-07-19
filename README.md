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

1. Iterate through pairs from `messages.txt` and `replies.txt`.
2. Randomly choose a username for the question and, if possible, a different one for the reply.
3. Send the question, wait 15 seconds and then send the matching reply.
4. Continue until 100 pairs have been sent or the lists are exhausted.
5. Sleep until midnight and start over.

The bot therefore sends up to 100 question/answer pairs every day at roughly
the same time.

## Troubleshooting

- Ensure the bot token and group ID in `.env` are correct.
- Add the bot to your Telegram group with permission to send messages.
- Check that `messages.txt`, `replies.txt` and `usernames.txt` exist and
  contain content.

### Expected behaviour

Once started, the bot posts each question from `messages.txt` followed by
its matching reply from `replies.txt`. The bot waits 15 seconds between
the question and the answer. After at most 100 pairs (or when the lists
end) it idles until the next day and then repeats.

## Running tests

The project includes a small pytest suite located in the `tests/` directory.
After installing the requirements you can execute the tests with:

```bash
pytest
```

This verifies that message files are loaded correctly and that the
scheduling logic waits 15 seconds between message pairs and stops after 100
pairs.

## Author
Developed by NAWA5

## License
This project is licensed under the [MIT License](LICENSE).
