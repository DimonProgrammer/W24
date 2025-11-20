"""Google Sheets client helpers for the Welcome24 bot."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Tuple

import gspread
from gspread import Worksheet
from gspread.utils import rowcol_to_a1

from config import BotConfig, load_config
from models import User, user_from_sheet_row

logger = logging.getLogger(__name__)

CONFIG: BotConfig = load_config()
USER_HEADER: List[str] = [
    "chat_id",
    "username",
    "first_name",
    "full_name",
    "phone",
    "city",
    "current_stage",
    "registered_at",
    "last_step_at",
    "reminder_1h_sent",
    "reminder_24h_sent",
]

DEFAULT_USER_VALUES: Dict[str, Any] = {
    "current_stage": CONFIG.start_stage,
    "reminder_1h_sent": False,
    "reminder_24h_sent": False,
}

_worksheet: Worksheet | None = None


def _init_worksheet() -> Worksheet:
    """Create and cache a gspread worksheet instance."""

    global _worksheet
    if _worksheet is not None:
        return _worksheet

    client = gspread.service_account_from_dict(CONFIG.google_service_account)
    spreadsheet = client.open_by_key(CONFIG.spreadsheet_id)
    _worksheet = spreadsheet.worksheet(CONFIG.worksheet_name)
    logger.info("Connected to worksheet '%s'", CONFIG.worksheet_name)
    return _worksheet


async def _get_worksheet() -> Worksheet:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _init_worksheet)


async def read_user(row_index: int) -> User | None:
    """Read a user by row index (1-based, including header)."""

    worksheet = await _get_worksheet()

    def _read() -> User | None:
        values = worksheet.row_values(row_index)
        if not values or len(values) < len(USER_HEADER):
            return None
        row_dict = dict(zip(USER_HEADER, values))
        return user_from_sheet_row(row_dict)

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _read)


async def create_user(data: Dict[str, Any]) -> User:
    """Create a new user entry in Google Sheets."""

    worksheet = await _get_worksheet()
    payload = {**DEFAULT_USER_VALUES, **data}
    record = _prepare_record(payload)

    def _append() -> None:
        worksheet.append_row(record, value_input_option="USER_ENTERED")

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _append)
    logger.info("Created user %s", data.get("chat_id"))
    return user_from_sheet_row(dict(zip(USER_HEADER, record)))


async def update_user(chat_id: int, updates: Dict[str, Any]) -> User | None:
    """Update an existing user entry."""

    record = await _find_user_record(chat_id)
    if record is None:
        logger.warning("User %s not found for update", chat_id)
        return None

    row_index, row_dict = record
    row_dict.update({key: value for key, value in updates.items() if key in USER_HEADER})
    sanitized_row = _prepare_record(row_dict)
    worksheet = await _get_worksheet()

    def _update() -> None:
        start = rowcol_to_a1(row_index, 1)
        end = rowcol_to_a1(row_index, len(USER_HEADER))
        worksheet.update(f"{start}:{end}", [sanitized_row])

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _update)
    logger.info("Updated user %s", chat_id)
    return user_from_sheet_row(dict(zip(USER_HEADER, sanitized_row)))


async def get_user_by_chat_id(chat_id: int) -> User | None:
    """Fetch a user by Telegram chat_id."""

    record = await _find_user_record(chat_id)
    if record is None:
        return None
    _, row_dict = record
    return user_from_sheet_row(row_dict)


async def get_user_by_username(username: str) -> User | None:
    """Find a user by @username."""

    normalized = username.lstrip("@").lower()
    users = await list_users()
    for user in users:
        if user.username and user.username.lower() == normalized:
            return user
    return None


async def list_users() -> List[User]:
    """Load all users from Google Sheets."""

    worksheet = await _get_worksheet()

    def _read() -> List[User]:
        records = worksheet.get_all_records()
        return [
            user_from_sheet_row(record)
            for record in records
            if record.get("chat_id")
        ]

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _read)


async def reset_user_progress(chat_id: int) -> User | None:
    """Reset a user's onboarding progress to stage_0."""

    return await update_user(
        chat_id,
        {
            "current_stage": "stage_0",
            "last_step_at": datetime.utcnow(),
            "reminder_1h_sent": False,
            "reminder_24h_sent": False,
        },
    )


async def _find_user_record(chat_id: int) -> Tuple[int, Dict[str, Any]] | None:
    worksheet = await _get_worksheet()

    def _lookup() -> Tuple[int, Dict[str, Any]] | None:
        records = worksheet.get_all_records()
        for idx, record in enumerate(records, start=2):  # data starts on row 2
            if str(record.get("chat_id")) == str(chat_id):
                return idx, record
        return None

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _lookup)


def _prepare_record(data: Dict[str, Any]) -> List[Any]:
    """Return a sanitized list that aligns with the user header order."""

    record: List[Any] = []
    for key in USER_HEADER:
        value = data.get(key)
        if isinstance(value, datetime):
            record.append(value.isoformat())
        elif isinstance(value, bool):
            record.append("TRUE" if value else "FALSE")
        elif value is None:
            record.append("")
        else:
            record.append(str(value))
    return record

