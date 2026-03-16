"""Medication data model."""

from dataclasses import dataclass, field
import uuid


@dataclass
class Medication:
    name: str
    description: str = ""
    form: str = "pill"
    pictogram_id: int | None = None
    custom_image_path: str | None = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "form": self.form,
            "pictogram_id": self.pictogram_id,
            "custom_image_path": self.custom_image_path,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data["name"],
            description=data.get("description", ""),
            form=data.get("form", "pill"),
            pictogram_id=data.get("pictogram_id"),
            custom_image_path=data.get("custom_image_path"),
        )
