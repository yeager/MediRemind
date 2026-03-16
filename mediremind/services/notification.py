"""System notification service."""

from gi.repository import Gio


class NotificationService:
    def __init__(self, app):
        self.app = app

    def send_reminder(self, medication):
        notification = Gio.Notification.new(_("Dags f\u00f6r medicin!"))
        notification.set_body(
            _("Det \u00e4r dags att ta: {name}").format(name=medication.name)
        )
        notification.set_priority(Gio.NotificationPriority.URGENT)
        notification.set_default_action("app.show-reminder")
        self.app.send_notification(f"reminder-{medication.id}", notification)

    def send_missed_alert(self, medication):
        notification = Gio.Notification.new(_("Missad dos!"))
        notification.set_body(
            _("{name} har inte bekr\u00e4ftats").format(name=medication.name)
        )
        notification.set_priority(Gio.NotificationPriority.URGENT)
        self.app.send_notification(f"missed-{medication.id}", notification)
