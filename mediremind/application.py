"""Main GTK4 Application class for MediRemind."""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, Gdk

from mediremind import __app_id__
from mediremind.services.persistence import PersistenceService
from mediremind.services.scheduler import SchedulerService
from mediremind.services.notification import NotificationService
from mediremind.services.alert_sender import AlertSender
from mediremind.window import MediRemindWindow


CSS = """
.med-card {
    padding: 12px;
    min-height: 100px;
}
.med-name {
    font-size: 24px;
    font-weight: bold;
}
.med-time {
    font-size: 20px;
}
.med-dosage {
    font-size: 18px;
}
.confirm-button {
    min-height: 80px;
    min-width: 200px;
    font-size: 20px;
}
.confirm-label {
    font-size: 20px;
    font-weight: bold;
}
.status-taken {
    background-color: #2ec27e;
}
.status-missed {
    background-color: #e01b24;
}
.status-overdue {
    background-color: #e5a50a;
}
.status-upcoming {
    background-color: #62a0ea;
}
.reminder-window {
    background-color: @window_bg_color;
}
.reminder-bell {
    font-size: 64px;
}
.reminder-title {
    font-size: 32px;
    font-weight: bold;
}
.reminder-med-name {
    font-size: 28px;
    font-weight: bold;
}
.reminder-dosage {
    font-size: 22px;
}
.snooze-button {
    min-height: 60px;
    font-size: 18px;
}
.pictogram-fallback {
    font-size: 64px;
}
.success {
    background-color: #2ec27e;
    color: white;
}
"""


class MediRemindApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id=__app_id__,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.persistence = None
        self.scheduler = None
        self.notification_service = None
        self.alert_sender = None
        self.window = None

    def do_startup(self):
        Adw.Application.do_startup(self)

        # Load CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_string(CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        # Initialize services
        self.persistence = PersistenceService()
        self.persistence.load_all()

        self.notification_service = NotificationService(self)
        self.alert_sender = AlertSender(self.persistence.settings)

        self.scheduler = SchedulerService(
            self.persistence,
            on_reminder=self._on_reminder,
            on_missed=self._on_missed,
        )
        self.scheduler.start()

        # Actions
        action = Gio.SimpleAction.new("show-reminder", None)
        action.connect("activate", self._on_show_reminder)
        self.add_action(action)

    def do_activate(self):
        if not self.window:
            self.window = MediRemindWindow(
                application=self,
                persistence=self.persistence,
                scheduler=self.scheduler,
            )
        self.window.present()

    def _on_reminder(self, medication, dose, entry):
        self.notification_service.send_reminder(medication)

        if self.persistence.settings.get("sound_enabled", True):
            try:
                from mediremind.utils.sound import play_reminder
                play_reminder()
            except Exception:
                pass

        if self.window:
            from mediremind.views.reminder_view import ReminderView
            reminder = ReminderView(self, medication, dose, entry)
            reminder.connect("dose-confirmed", self._on_reminder_confirmed, entry)
            reminder.connect("dose-snoozed", self._on_reminder_snoozed, dose, entry)
            reminder.present()

    def _on_reminder_confirmed(self, view, entry):
        try:
            from mediremind.utils.sound import stop_reminder
            stop_reminder()
        except Exception:
            pass
        self.scheduler.confirm_dose(entry)
        if self.window:
            self.window.refresh_schedule()

    def _on_reminder_snoozed(self, view, dose, entry):
        try:
            from mediremind.utils.sound import stop_reminder
            stop_reminder()
        except Exception:
            pass
        GLib.timeout_add_seconds(300, self._snooze_callback, dose, entry)

    def _snooze_callback(self, dose, entry):
        med = self.persistence.get_medication_by_id(dose.medication_id)
        if med and entry.status == "pending":
            self._on_reminder(med, dose, entry)
        return False

    def _on_missed(self, entry):
        med = self.persistence.get_medication_by_id(entry.medication_id)
        if med:
            self.notification_service.send_missed_alert(med)
            success = self.alert_sender.send_missed_alert(med, entry.scheduled_time)
            entry.alert_sent = success
            self.persistence.save_history()
        if self.window:
            self.window.refresh_schedule()

    def _on_show_reminder(self, action, parameter):
        if self.window:
            self.window.present()

    def do_shutdown(self):
        if self.scheduler:
            self.scheduler.stop()
        Adw.Application.do_shutdown(self)
