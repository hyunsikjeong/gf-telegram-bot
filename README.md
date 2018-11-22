# gf-telegram-bot
Telegram bot for Girls' Frontline (Korean version)

Telegram ID: `@girlsfrontline_krbot` ([Link](https://telegram.me/girlsfrontline_krbot))

## Requirements

The bot uses [oauth2](https://github.com/joestump/python-oauth2) and [python-telegram-bot](https://python-telegram-bot.org). (No more using tweepy, because it is not maintained.)

You can install requirements by:

```
pip install -r requirements.txt
```

Or, you can install one by one from the repositories.

The bot is tested in Python 3.6 and 3.7. But as the documentation of oauth2, it is recommended to run the bot in Python 3.3 and 3.4.

## How to run

You'll need Twitter API keys/secrets and Telegram bot token, and the Twitter bot ID to track. This information should be written in `setting.json`.

To write `setting.json`, just copy `setting_example.json` to the `setting.json`.

The format is:

```json
{
    "tg_token": "Your telegram bot token",
    "tw_consumer_key": "Your Twitter consumer key",
    "tw_consumer_secret": "Your Twitter consumer secret key",
    "tw_access_token": "Your Twitter access token",
    "tw_access_secret": "Your Twitter access secret token",
    "tw_gf_bot_id": "girlsfrontlinek"
}
```

After writing the `setting.json`, run the bot by `python start.py`.

## Special contributors

There are contributors who helped to write the bot at first, especially in making the database.

- [Onedict](https://github.com/onedict)([Twitter](0nestation))
- Zion.Jair([Twitter](https://twitter.com/chlwodud30))
- LAVIS([Twitter](https://twitter.com/LAVIS__CANNON))
- Kirsi([Twitter](https://twitter.com/DevelopKirsi))

Thank you for your efforts!