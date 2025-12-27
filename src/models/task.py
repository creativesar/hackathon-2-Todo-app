"""Task model - simple data class."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
