"""GTK4/Adwaita application."""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio

from mediremind.reminder import ReminderManager
from mediremind.window import MediRemindWindow


class MediRemindApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="se.mediremind.app")
        self.reminder = ReminderManager(self)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MediRemindWindow(self, self.reminder)
        self.reminder.start()
        win.present()

    def do_shutdown(self):
        self.reminder.stop()
        Adw.Application.do_shutdown(self)
