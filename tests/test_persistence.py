"""Tests for persistence service."""

import unittest
import tempfile
import os

from mediremind.models.medication import Medication
from mediremind.models.dose import DoseSchedule
from mediremind.models.history_entry import HistoryEntry
from mediremind.services.persistence import PersistenceService


class TestPersistenceService(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.service = PersistenceService()
        self.service.data_dir = self.tmpdir
        self.service.schedule_file = os.path.join(self.tmpdir, "schedule.json")
        self.service.history_file = os.path.join(self.tmpdir, "history.json")
        self.service.settings_file = os.path.join(self.tmpdir, "settings.json")

    def test_save_and_load_schedule(self):
        med = Medication(name="Test Med", form="pill")
        dose = DoseSchedule(medication_id=med.id, times=["09:00"])
        self.service.medications = [med]
        self.service.doses = [dose]
        self.service.save_schedule()

        service2 = PersistenceService()
        service2.data_dir = self.tmpdir
        service2.schedule_file = self.service.schedule_file
        service2.history_file = self.service.history_file
        service2.settings_file = self.service.settings_file
        service2._load_schedule()

        self.assertEqual(len(service2.medications), 1)
        self.assertEqual(service2.medications[0].name, "Test Med")
        self.assertEqual(len(service2.doses), 1)

    def test_save_and_load_history(self):
        entry = HistoryEntry(
            dose_id="d1",
            medication_id="m1",
            scheduled_time="2026-03-16T08:00:00",
            status="taken",
        )
        self.service.history = [entry]
        self.service.save_history()

        service2 = PersistenceService()
        service2.data_dir = self.tmpdir
        service2.history_file = self.service.history_file
        service2._load_history()

        self.assertEqual(len(service2.history), 1)
        self.assertEqual(service2.history[0].status, "taken")

    def test_backup_created(self):
        self.service.medications = []
        self.service.doses = []
        self.service.save_schedule()
        self.service.save_schedule()
        self.assertTrue(os.path.exists(self.service.schedule_file + ".bak"))

    def test_get_medication_by_id(self):
        med = Medication(name="Alvedon")
        self.service.medications = [med]
        found = self.service.get_medication_by_id(med.id)
        self.assertEqual(found.name, "Alvedon")
        self.assertIsNone(self.service.get_medication_by_id("nonexistent"))


if __name__ == "__main__":
    unittest.main()
