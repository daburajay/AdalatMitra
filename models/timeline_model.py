"""
models/timeline_model.py
Defines a single timeline event — used by timeline_agent.py to build
the chronological view of a case shown in the UI.
"""

from dataclasses import dataclass


@dataclass
class TimelineEvent:
    event_date: str
    event_title: str
    event_description: str

    def to_dict(self) -> dict:
        return {
            "event_date": self.event_date,
            "event_title": self.event_title,
            "event_description": self.event_description,
        }
