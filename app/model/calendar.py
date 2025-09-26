from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import ClassVar

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error

@dataclass
class Reminder:
    EMAIL: ClassVar[str] = 'email'
    SYSTEM: ClassVar[str] = 'system'

    date_time: datetime
    type: str = EMAIL

    def __str__(self):
        return f"Reminder on {self.date_time} of type {self.type}"

@dataclass
class Event:
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    reminders: list[Reminder] = field(init=False, default_factory=list)
    id: str = field(default_factory=generate_unique_id)

    def add_reminder(self, date_tiime: datetime, type: str = Reminder.EMAIL) -> None:
        reminder = Reminder(date_tiime, type)
        self.reminders.append(reminder)

    def delete_reminder(self, reminder_index: int) -> None:
        if reminder_index >= len(self.reminders):
            reminder_not_found_error()
        else:
            for reminder in range(len(self.reminders)):
                if reminder == reminder_index:
                    self.reminders.pop(reminder)

    def __str__(self) -> str:
        return f'ID: {self.id}\nEvent title: {self.title}\nDescription: {self.description}\nTime: {self.start_at} - {self.end_at}'



class Day:
    def __init__(self, date: date) -> None:
        self.date: date = date
        self.slots: dict[time, str | None] = {}
        self._init_slots()

    def _init_slots(self) -> None:
        self.slots = {}
        for hour in range(24):
            for minute in range(0,60,15):
                self.slots[(hour, minute)] = None
