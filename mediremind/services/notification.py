"""System notification service."""

from gi.repository import Gio


class NotificationService:
    def __init__(self, app):
        self.app = app

    def send_reminder(self, medication):
        notification = Gio.Notification.new(_("Time for medicine!"))
        notification.set_body(
            _("It is time to take: {name}").format(name=medication.name)
        )
        notification.set_priority(Gio.NotificationPriority.URGENT)
        notification.set_default_action("app.show-reminder")
        self.app.send_notification(f"reminder-{medication.id}", notification)

    def send_missed_alert(self, medication):
        notification = Gio.Notification.new(_("Missad dos!"))
        notification.set_body(
            _("{name} has not been confirmed").format(name=medication.name)
        )
        notification.set_priority(Gio.NotificationPriority.URGENT)
        self.app.send_notification(f"missed-{medication.id}", notification)
