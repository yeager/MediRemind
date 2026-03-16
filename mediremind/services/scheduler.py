"""Reminder scheduler using GLib timeouts."""

from datetime import datetime
from gi.repository import GLib
from mediremind.models.history_entry import HistoryEntry


class SchedulerService:
    def __init__(self, persistence, on_reminder=None, on_missed=None):
        self.persistence = persistence
        self.on_reminder = on_reminder
        self.on_missed = on_missed
        self._missed_sources = {}
        self._check_source = None

    def start(self):
        self._check_source = GLib.timeout_add_seconds(30, self._check_doses)

    def stop(self):
        for source_id in self._missed_sources.values():
            GLib.source_remove(source_id)
        self._missed_sources.clear()
        if self._check_source:
            GLib.source_remove(self._check_source)
            self._check_source = None

    def _check_doses(self):
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")

        for dose in self.persistence.doses:
            if not dose.active:
                continue
            if dose.days and now.weekday() not in dose.days:
                continue

            for time_str in dose.times:
                scheduled_dt = f"{today_str}T{time_str}:00"
                already_handled = any(
                    h.dose_id == dose.id and h.scheduled_time == scheduled_dt
                    for h in self.persistence.history
                )
                if already_handled:
                    continue
                if current_time == time_str:
                    self._fire_reminder(dose, scheduled_dt)

        return True

    def _fire_reminder(self, dose, scheduled_dt):
        med = self.persistence.get_medication_by_id(dose.medication_id)
        if not med:
            return

        entry = HistoryEntry(
            dose_id=dose.id,
            medication_id=dose.medication_id,
            scheduled_time=scheduled_dt,
            status="pending",
        )
        self.persistence.add_history_entry(entry)

        if self.on_reminder:
            self.on_reminder(med, dose, entry)

        timeout_min = self.persistence.settings.get("missed_timeout_minutes", 30)
        source_id = GLib.timeout_add_seconds(
            timeout_min * 60, self._on_missed_timeout, entry,
        )
        self._missed_sources[entry.id] = source_id

    def _on_missed_timeout(self, entry):
        if entry.status == "pending":
            entry.mark_missed()
            self.persistence.save_history()
            if self.on_missed:
                self.on_missed(entry)
        self._missed_sources.pop(entry.id, None)
        return False

    def confirm_dose(self, entry):
        entry.mark_taken()
        self.persistence.save_history()
        source_id = self._missed_sources.pop(entry.id, None)
        if source_id:
            GLib.source_remove(source_id)

    def get_todays_schedule(self):
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        result = []

        for dose in self.persistence.doses:
            if not dose.active:
                continue
            if dose.days and now.weekday() not in dose.days:
                continue

            med = self.persistence.get_medication_by_id(dose.medication_id)
            if not med:
                continue

            for time_str in dose.times:
                scheduled_dt = f"{today_str}T{time_str}:00"
                history_entry = None
                for h in self.persistence.history:
                    if h.dose_id == dose.id and h.scheduled_time == scheduled_dt:
                        history_entry = h
                        break
                result.append((med, dose, time_str, history_entry))

        result.sort(key=lambda x: x[2])
        return result
