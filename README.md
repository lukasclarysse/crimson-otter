# Crimson Otter

A lightweight, modular Discord honeypot bot.

Crimson Otter monitors a designated channel and automatically moderates anyone who posts there. When triggered, it deletes the message, optionally purges recent user activity, and executes a configured moderation action (kick or ban).

---

## Features

- **Honeypot Channel:** Automatic detection and moderation for restricted channels.
- **Configurable Actions:** Action member removal via `kick` or `ban`.
- **Message Purging:** Automatically cleans up recent messages upon trigger.
- **Audit Logging:** Sends event notifications to a designated log channel.
- **Modular Architecture:** Features are implemented as independent modules.
- **Container Ready:** Full Docker and Docker Compose support.

---

## Prerequisites

### Requirements
- **Privileged Intents:** Message Content Intent, Server Members Intent
- **Bot Permissions:** Send Messages, Embed Links, Read Message History, Manage Messages, Kick Members, Ban Members

### Environment Support
- **Docker Deployment:** Docker & Docker Compose
- **Local Deployment:** Python 3.13+

---

## Configuration

Create a `.env` file in the project root:

```env
TOKEN=yourbottoken
GUILD_ID=yourserverid
HONEYPOT_CHANNEL=yourhoneypotchannelid
LOG_CHANNEL=yourlogchannelid
BOT_ACTION=kick
PURGE_TIMEFRAME=300
```

### Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `TOKEN` | Discord bot token | — |
| `GUILD_ID` | Target Discord server ID | — |
| `HONEYPOT_CHANNEL` | Channel ID monitored as honeypot | — |
| `LOG_CHANNEL` | Channel ID for moderation logs | — |
| `BOT_ACTION` | Action to perform (`kick` or `ban`) | — |
| `PURGE_TIMEFRAME` | Timeframe in seconds to purge recent messages | `300` |

> **Security Note:** Keep `.env` secure and uncommitted. It is excluded via `.gitignore` and `.dockerignore`.

---

## Deployment

### Docker (Recommended)

Published Image: `lukasclarysse/crimson-otter:latest`

#### Docker Compose
```bash
docker compose up -d      # Start containers
docker compose logs -f    # View logs
docker compose restart    # Restart bot
docker compose down       # Stop containers
```

#### Build & Run Manually
```bash
# Build image
docker build -t crimson-otter .

# Run container (Linux / macOS / Windows)
docker run -d --name crimson-otter --env-file .env --restart unless-stopped crimson-otter
```

---

### Local Development

1. **Set up virtual environment:**
   ```bash
   python -m venv .venv
   ```
   * *Windows:* `.venv\Scripts\activate`
   * *Linux / macOS:* `source .venv/bin/activate`

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch application:**
   ```bash
   python src/bot.py
   ```
   > Verify status by sending `$ping` in a server channel.

---

## Developer Guide

- **Architecture:** Modules reside in `src/modules/` and are automatically loaded at runtime.
- **Base Image:** Built on `python:3.13-slim`, copying `src/` and dependencies from `requirements.txt`.
- **Ignore Rules:** `.dockerignore` excludes local secrets, virtual environments, Git metadata, and Python cache.