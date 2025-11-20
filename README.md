## Welcome24 Telegram Bot

Async onboarding bot for Welcome24 built on `aiogram 3.x`, Google Sheets, and aiohttp webhooks. The bot registers new agents, walks them through 12 onboarding stages, sends reminders, and exposes admin tooling for support teams.

### Requirements
- Python 3.10+
- Google Cloud service-account JSON with access to the onboarding spreadsheet
- Telegram bot token

Install dependencies:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables
Use `env.template` as a base:
```
cp env.template .env
```

| Variable | Description |
| --- | --- |
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather |
| `GOOGLE_SHEETS_CREDENTIALS_JSON` | Path or JSON for the service account |
| `GOOGLE_SPREADSHEET_ID` | Spreadsheet ID that stores user records |
| `GOOGLE_WORKSHEET_NAME` | Worksheet/tab name, default `Users` |
| `ADMIN_CHAT_ID` | Telegram user ID allowed to run admin commands |
| `WEBHOOK_URL` | (Render/Vercel) HTTPS URL like `https://app.onrender.com/webhook` |
| `HOST`, `PORT` | Host/port for the aiohttp server (default `0.0.0.0:8000`) |

### Google Sheets Schema
Create a worksheet with headers in this order:
`chat_id, username, first_name, full_name, phone, city, current_stage, registered_at, last_step_at, reminder_1h_sent, reminder_24h_sent`

### Running Locally (Polling)
1. Leave `WEBHOOK_URL` empty in `.env`.
2. Activate the virtual environment and run:
   ```bash
   python main.py
   ```
3. The bot removes any webhook, starts long-polling, and attaches all handlers. Use this mode for development/testing.

### Deploying on Render / Vercel (Webhook)
1. Set `WEBHOOK_URL` to your public HTTPS endpoint (e.g. `https://welcome24.onrender.com/webhook`).
2. Configure the Render service:
   - Runtime: Python 3.10+
   - Start command: `python main.py`
   - Expose port `8000` (Render sets `PORT`; the app reads it automatically).
3. On boot the bot calls `setWebhook(WEBHOOK_URL)`, spins up an `aiohttp` app (`web.Application()` + `setup_application`) and serves updates via `web.run_app(app, port=PORT)`.
4. Verify logs show “Starting webhook mode”.

### Admin & Reminders
- `/progress @username` – show user status
- `/reset @username` – reset to stage 0 and resend stage intro
- `/broadcast текст` – message every user with 150 ms anti-flood
- Reminder scheduler runs every 10 minutes, nudging users who paused 1h/24h ago, and stops automatically on shutdown.

### Project Structure
```
handlers/
  admin.py        # admin commands
  callbacks.py    # inline buttons & stage transitions
  registration.py # /start onboarding FSM
  reminders.py    # background reminder loop
  stages.py       # shared stage rendering helpers
config.py         # env loader
constants.py      # stage texts, buttons, video/file placeholders
main.py           # polling/webhook bootstrap
models.py         # User dataclass + parsers
sheets_client.py  # Google Sheets CRUD helpers
requirements.txt
env.template
```

### Development Tips
- Logs go to stdout; use Render log stream for production support.
- Reminder flags (`reminder_1h_sent`, `reminder_24h_sent`) reset automatically whenever a user progresses.
- Add real video/file IDs in `constants.py` once assets are ready.

