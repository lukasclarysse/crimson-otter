# Crimson Otter

A small Discord honeypot bot.

Crimson Otter watches a designated channel and treats anyone who posts there as having triggered the honeypot. Their message is deleted, recent messages can be purged, and they can be kicked or banned depending on the configuration.

It started as a simple moderation bot and is intentionally kept fairly small. The bot is modular, so new features can be added as their own modules without having to pile everything into one giant file.

## Features

- Honeypot channel with automatic moderation
- Configurable kick or ban action
- Recent message purging
- Moderation logs
- Modular feature system

## Setup

### Requirements

- Python 3.10+
- A Discord bot application
- A bot token

The bot needs the **Message Content** and **Members** privileged intents enabled in the Discord Developer Portal.

It also needs permission to:

- Send messages
- Embed links
- Read message history
- Manage messages
- Kick or ban members

### Install

Clone the repository and install the dependencies:
```bash
git clone https://github.com/lukasclarysse/crimson-otter.git
cd crimson-otter
python -m venv .venv
```
Activate the virtual environment.
```
.venv\Scripts\activate      # windows
source .venv/bin/activate   # unix
```

Then install the dependencies:
```python
pip install -r requirements.txt
```

### Configure

Create a `.env` file in the project root:
```plaintext
TOKEN=yourbottoken
GUILDID=yourserverid
HONEYPOTCHANNEL=yourhoneypotchannelid
LOGCHANNEL=yourlogchannel_id
BOTACTION=kick
PURGETIMEFRAME=300
```

`BOT_ACTION` can be either `kick` or `ban`.

`PURGE_TIMEFRAME` is the number of seconds of recent messages to remove when the honeypot is triggered.

### Run

Start the bot with:

python src/bot.py

If everything is working, the bot will come online and `$ping` should return its current latency.

