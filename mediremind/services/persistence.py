"""JSON-based data persistence for schedule and history."""

import json
import os
import shutil
from datetime import datetime

from mediremind.models.medication import Medication
from mediremind.models.dose import DoseSchedule
from mediremind.models.history_entry import HistoryEntry
from mediremind.utils.paths import get_data_dir


class PersistenceService:
    def __init__(self):
        self.data_dir = get_data_dir()
        self.schedule_file = os.path.join(self.data_dir, "schedule.json")
        self.history_file = os.path.join(self.data_dir, "history.json")
        self.settings_file = os.path.join(self.data_dir, "settings.json")

        self.medications: list[Medication] = []
        self.doses: list[DoseSchedule] = []
        self.history: list[HistoryEntry] = []
        self.settings: dict = {}

    def load_all(self):
        self._load_schedule()
        self._load_history()
        self._load_settings()

    def _load_schedule(self):
        if not os.path.exists(self.schedule_file):
            self._create_sample_data()
            return
        with open(self.schedule_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.medications = [Medication.from_dict(m) for m in data.get("medications", [])]
        self.doses = [DoseSchedule.from_dict(d) for d in data.get("doses", [])]

    def _load_history(self):
        if not os.path.exists(self.history_file):
            self.history = []
            return
        with open(self.history_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.history = [HistoryEntry.from_dict(h) for h in data.get("entries", [])]

    def _load_settings(self):
        if not os.path.exists(self.settings_file):
            self.settings = {
                "contact_name": "",
                "contact_email": "",
                "contact_phone": "",
                "smtp_server": "",
                "smtp_port": 587,
                "smtp_user": "",
                "smtp_password": "",
                "sms_api_key": "",
                "sms_api_url": "",
                "missed_timeout_minutes": 30,
                "language": "sv",
                "sound_enabled": True,
            }
            self.save_settings()
            return
        with open(self.settings_file, "r", encoding="utf-8") as f:
            self.settings = json.load(f)

    def save_schedule(self):
        self._backup(self.schedule_file)
        data = {
            "medications": [m.to_dict() for m in self.medications],
            "doses": [d.to_dict() for d in self.doses],
        }
        with open(self.schedule_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_history(self):
        self._backup(self.history_file)
        data = {"entries": [h.to_dict() for h in self.history]}
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_settings(self):
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2, ensure_ascii=False)

    def _backup(self, filepath):
        if os.path.exists(filepath):
            shutil.copy2(filepath, filepath + ".bak")

    def add_history_entry(self, entry: HistoryEntry):
        self.history.append(entry)
        self.save_history()

    def get_medication_by_id(self, med_id: str):
        for m in self.medications:
            if m.id == med_id:
                return m
        return None

    def get_doses_for_medication(self, med_id: str):
        return [d for d in self.doses if d.medication_id == med_id]

    def get_today_history(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return [h for h in self.history if h.scheduled_time.startswith(today)]

    def _create_sample_data(self):
        med1 = Medication(name="Alvedon", description="Sm\u00e4rtstillande", form="pill")
        med2 = Medication(name="Omeprazol", description="Magsyrah\u00e4mmare", form="pill")
        med3 = Medication(name="\u00d6gondroppar", description="Mot torra \u00f6gon", form="drops")

        self.medications = [med1, med2, med3]
        self.doses = [
            DoseSchedule(medication_id=med1.id, times=["08:00", "20:00"], dosage="2 tabletter"),
            DoseSchedule(medication_id=med2.id, times=["07:00"], dosage="1 kapsel"),
            DoseSchedule(medication_id=med3.id, times=["08:00", "14:00", "20:00"], dosage="2 droppar per \u00f6ga"),
        ]
        self.save_schedule()
