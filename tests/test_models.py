"""Tests for data models."""

import unittest
from mediremind.models.medication import Medication
from mediremind.models.dose import DoseSchedule
from mediremind.models.history_entry import HistoryEntry


class TestMedication(unittest.TestCase):
    def test_create_medication(self):
        med = Medication(name="Alvedon", form="pill")
        self.assertEqual(med.name, "Alvedon")
        self.assertEqual(med.form, "pill")
        self.assertIsNotNone(med.id)

    def test_serialization(self):
        med = Medication(name="Test", description="Desc", form="drops")
        data = med.to_dict()
        restored = Medication.from_dict(data)
        self.assertEqual(med.name, restored.name)
        self.assertEqual(med.id, restored.id)
        self.assertEqual(med.form, restored.form)


class TestDoseSchedule(unittest.TestCase):
    def test_create_dose(self):
        dose = DoseSchedule(medication_id="abc", times=["08:00", "20:00"])
        self.assertEqual(len(dose.times), 2)
        self.assertTrue(dose.active)

    def test_serialization(self):
        dose = DoseSchedule(
            medication_id="abc",
            times=["08:00"],
            dosage="2 tabletter",
        )
        data = dose.to_dict()
        restored = DoseSchedule.from_dict(data)
        self.assertEqual(dose.medication_id, restored.medication_id)
        self.assertEqual(dose.dosage, restored.dosage)


class TestHistoryEntry(unittest.TestCase):
    def test_mark_taken(self):
        entry = HistoryEntry(
            dose_id="d1",
            medication_id="m1",
            scheduled_time="2026-03-16T08:00:00",
        )
        entry.mark_taken()
        self.assertEqual(entry.status, "taken")
        self.assertIsNotNone(entry.confirmed_time)

    def test_mark_missed(self):
        entry = HistoryEntry(
            dose_id="d1",
            medication_id="m1",
            scheduled_time="2026-03-16T08:00:00",
        )
        entry.mark_missed()
        self.assertEqual(entry.status, "missed")


if __name__ == "__main__":
    unittest.main()
