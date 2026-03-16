"""History entry data model for dose confirmations."""

from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class HistoryEntry:
    dose_id: str
    medication_id: str
    scheduled_time: str
    status: str = "pending"
    confirmed_time: str | None = None
    alert_sent: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return {
            "id": self.id,
            "dose_id": self.dose_id,
            "medication_id": self.medication_id,
            "scheduled_time": self.scheduled_time,
            "status": self.status,
            "confirmed_time": self.confirmed_time,
            "alert_sent": self.alert_sent,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            dose_id=data["dose_id"],
            medication_id=data["medication_id"],
            scheduled_time=data["scheduled_time"],
            status=data.get("status", "pending"),
            confirmed_time=data.get("confirmed_time"),
            alert_sent=data.get("alert_sent", False),
        )

    def mark_taken(self):
        self.status = "taken"
        self.confirmed_time = datetime.now().isoformat()

    def mark_missed(self):
        self.status = "missed"
