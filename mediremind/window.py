"""Main application window."""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from mediremind.views.schedule_view import ScheduleView
from mediremind.views.history_view import HistoryView
from mediremind.views.settings_view import SettingsView


class MediRemindWindow(Adw.ApplicationWindow):
    def __init__(self, application, persistence, scheduler):
        super().__init__(
            application=application,
            title="MediRemind",
            default_width=600,
            default_height=800,
        )
        self.persistence = persistence
        self.scheduler = scheduler

        # Main layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Header bar
        header = Adw.HeaderBar()
        header.set_title_widget(Gtk.Label(label="MediRemind"))
        main_box.append(header)

        # View stack
        self.stack = Adw.ViewStack()

        # Schedule view
        self.schedule_view = ScheduleView(scheduler, persistence)
        self.stack.add_titled_with_icon(
            self.schedule_view,
            "schedule",
            _("Schema"),
            "view-list-symbolic",
        )

        # History view
        self.history_view = HistoryView(persistence)
        self.stack.add_titled_with_icon(
            self.history_view,
            "history",
            _("Historik"),
            "document-open-recent-symbolic",
        )

        # Settings view
        self.settings_view = SettingsView(
            persistence,
            on_schedule_changed=self.refresh_schedule,
        )
        self.stack.add_titled_with_icon(
            self.settings_view,
            "settings",
            _("Inställningar"),
            "emblem-system-symbolic",
        )

        main_box.append(self.stack)

        # Bottom navigation
        switcher_bar = Adw.ViewSwitcherBar()
        switcher_bar.set_stack(self.stack)
        switcher_bar.set_reveal(True)
        main_box.append(switcher_bar)

        self.set_content(main_box)

    def refresh_schedule(self):
        self.schedule_view.refresh()

    def refresh_history(self):
        self.history_view.refresh()
