"""Dose schedule data model."""

from dataclasses import dataclass, field
import uuid


@dataclass
class DoseSchedule:
    medication_id: str
    times: list[str] = field(default_factory=lambda: ["08:00"])
    days: list[int] = field(default_factory=list)
    dosage: str = "1 tablett"
    active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return {
            "id": self.id,
            "medication_id": self.medication_id,
            "times": self.times,
            "days": self.days,
            "dosage": self.dosage,
            "active": self.active,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            medication_id=data["medication_id"],
            times=data.get("times", ["08:00"]),
            days=data.get("days", []),
            dosage=data.get("dosage", "1 tablett"),
            active=data.get("active", True),
        )
