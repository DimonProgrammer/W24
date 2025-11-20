"""Configuration utilities for the Welcome24 Telegram bot."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


def _load_json_from_env(env_value: str) -> Dict[str, Any]:
    """Try to parse JSON directly or read it from a file path."""

    candidate = env_value.strip()
    if candidate.startswith("{"):
        return json.loads(candidate)

    path = Path(candidate)
    if not path.exists():
        raise ValueError(f"Credentials file '{candidate}' not found")

    return json.loads(path.read_text(encoding="utf-8"))


@dataclass(slots=True)
class BotConfig:
    """Runtime configuration loaded from environment variables."""

    telegram_token: str
    google_service_account: Dict[str, Any]
    spreadsheet_id: str
    worksheet_name: str
    start_stage: str
    admin_chat_id: int | None
    webhook_url: str | None
    listen_host: str
    listen_port: int


def load_config() -> BotConfig:
    """Load configuration from environment variables."""

    telegram_token = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_token:
        raise ValueError("TELEGRAM_TOKEN / TELEGRAM_BOT_TOKEN is not set")

    credentials_env = (
        os.getenv("GOOGLE_SHEETS_CONFIG")
        or os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        or os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON")
    )
    if not credentials_env:
        raise ValueError("Google Sheets credentials are not set")

    try:
        service_account_data: Dict[str, Any] = _load_json_from_env(credentials_env)
    except json.JSONDecodeError as exc:
        raise ValueError("Provided Google credentials are not valid JSON") from exc

    spreadsheet_id = os.getenv("GOOGLE_SPREADSHEET_ID")
    if not spreadsheet_id:
        raise ValueError("GOOGLE_SPREADSHEET_ID is not set")

    worksheet_name = os.getenv("GOOGLE_WORKSHEET_NAME", "Users")
    start_stage = os.getenv("BOT_START_STAGE", "stage_0")
    webhook_url = os.getenv("WEBHOOK_URL")

    admin_raw = os.getenv("ADMIN_CHAT_ID")
    try:
        admin_chat_id = int(admin_raw) if admin_raw else None
    except ValueError:
        raise ValueError("ADMIN_CHAT_ID must be an integer") from None

    listen_host = os.getenv("HOST", "0.0.0.0")
    listen_port = int(os.getenv("PORT", "8000"))

    return BotConfig(
        telegram_token=telegram_token,
        google_service_account=service_account_data,
        spreadsheet_id=spreadsheet_id,
        worksheet_name=worksheet_name,
        start_stage=start_stage,
        admin_chat_id=admin_chat_id,
        webhook_url=webhook_url,
        listen_host=listen_host,
        listen_port=listen_port,
    )

