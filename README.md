# cpsc408_Discord_MovieDatabase

## Developing discord bot

1. Clone repo
2. Set up python virtual environment

```bash
python3 -m venv venv          # create virtual environment just once
source ./venv/bin/activate    # activate virtual environment
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

3. Set up environment variables

```bash
# .env
DISCORD_BOT_TOKEN=<discord_bot_token>
```

I (@christofuyy) created the bot, so ask me for the token. If you aren't
aware already, secrets should never be committed to version control, so don't commit
your `.env` file. But you don't have to worry because it's already ignored in
the `.gitignore` file.

4. Develop and test your changes

```bash
python bot.py
```

5. Update `requirements.txt` if you installed new dependencies

```bash
pip freeze > requirements.txt
```
