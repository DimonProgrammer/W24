"""Domain models for the Welcome24 bot."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


@dataclass(slots=True)
class User:
    """Dataclass representation of a bot user stored in Google Sheets."""

    chat_id: int
    username: str | None = None
    first_name: str | None = None
    full_name: str | None = None
    phone: str | None = None
    city: str | None = None
    current_stage: str | None = None
    registered_at: datetime | None = None
    last_step_at: datetime | None = None
    reminder_1h_sent: bool = False
    reminder_24h_sent: bool = False

    def to_sheet_row(self) -> List[Any]:
        """Return the user data ordered for Google Sheets append/update operations."""

        return [
            str(self.chat_id),
            self.username or "",
            self.first_name or "",
            self.full_name or "",
            self.phone or "",
            self.city or "",
            self.current_stage or "",
            self._datetime_to_str(self.registered_at),
            self._datetime_to_str(self.last_step_at),
            self._bool_to_str(self.reminder_1h_sent),
            self._bool_to_str(self.reminder_24h_sent),
        ]

    def to_sheet_dict(self) -> Dict[str, Any]:
        """Return a dictionary matching the Google Sheets header names."""

        return {
            "chat_id": str(self.chat_id),
            "username": self.username or "",
            "first_name": self.first_name or "",
            "full_name": self.full_name or "",
            "phone": self.phone or "",
            "city": self.city or "",
            "current_stage": self.current_stage or "",
            "registered_at": self._datetime_to_str(self.registered_at),
            "last_step_at": self._datetime_to_str(self.last_step_at),
            "reminder_1h_sent": self._bool_to_str(self.reminder_1h_sent),
            "reminder_24h_sent": self._bool_to_str(self.reminder_24h_sent),
        }

    @staticmethod
    def _datetime_to_str(value: datetime | None) -> str:
        return value.isoformat() if value else ""

    @staticmethod
    def _bool_to_str(value: bool) -> str:
        return "TRUE" if value else "FALSE"


def user_from_sheet_row(row: Dict[str, Any]) -> User:
    """Convert a Google Sheets row (dict) into a User dataclass."""

    return User(
        chat_id=int(row.get("chat_id", 0)),
        username=row.get("username") or None,
        first_name=row.get("first_name") or None,
        full_name=row.get("full_name") or None,
        phone=row.get("phone") or None,
        city=row.get("city") or None,
        current_stage=row.get("current_stage") or None,
        registered_at=_parse_datetime(row.get("registered_at")),
        last_step_at=_parse_datetime(row.get("last_step_at")),
        reminder_1h_sent=_parse_bool(row.get("reminder_1h_sent")),
        reminder_24h_sent=_parse_bool(row.get("reminder_24h_sent")),
    )


def _parse_datetime(raw_value: Any) -> datetime | None:
    if not raw_value:
        return None
    if isinstance(raw_value, datetime):
        return raw_value
    try:
        return datetime.fromisoformat(str(raw_value))
    except ValueError:
        return None


def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "1", "yes"}

