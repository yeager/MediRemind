"""Notification timer for medication reminders."""

from datetime import datetime

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("GLib", "2.0")
from gi.repository import Gio, GLib

from mediremind import _


class ReminderManager:
    """Checks medication times and sends desktop notifications."""

    def __init__(self, app):
        self.app = app
        self.medications = []
        self._fired = set()
        self._today = datetime.now().strftime("%Y-%m-%d")
        self._timer_id = None

    def update(self, medications: list[dict]):
        self.medications = list(medications)

    def start(self):
        if self._timer_id is None:
            self._timer_id = GLib.timeout_add_seconds(30, self._check)

    def stop(self):
        if self._timer_id is not None:
            GLib.source_remove(self._timer_id)
            self._timer_id = None

    def _check(self) -> bool:
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")

        if today != self._today:
            self._fired.clear()
            self._today = today

        for med in self.medications:
            key = (med["name"], med["time"], today)
            if med["time"] == current_time and key not in self._fired:
                self._fired.add(key)
                self._send_notification(med["name"])

        return True  # keep timer running

    def _send_notification(self, name: str):
        notification = Gio.Notification.new(_("Medication Reminder"))
        notification.set_body(_("Time to take %s") % name)
        notification.set_priority(Gio.NotificationPriority.HIGH)
        self.app.send_notification(f"mediremind-{name}", notification)
