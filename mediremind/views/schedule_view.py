"""Main schedule view showing today's medication doses."""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk

from mediremind.widgets.med_card import MedCard
from mediremind.services.pictogram import PictogramService


class ScheduleView(Gtk.Box):
    """Daily schedule list with medication cards."""

    def __init__(self, scheduler, persistence):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.scheduler = scheduler
        self.persistence = persistence
        self.pictogram_service = PictogramService()

        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        header_box.set_margin_top(16)
        header_box.set_margin_bottom(8)
        header_box.set_margin_start(16)
        header_box.set_margin_end(16)

        title = Gtk.Label(label=_("Today's medicines"))
        title.add_css_class("title-1")
        title.set_halign(Gtk.Align.START)
        header_box.append(title)

        from datetime import datetime
        date_label = Gtk.Label(
            label=datetime.now().strftime("%A %d %B %Y").capitalize()
        )
        date_label.add_css_class("dim-label")
        date_label.set_halign(Gtk.Align.START)
        header_box.append(date_label)

        self.append(header_box)

        # Scrolled list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.list_box.add_css_class("boxed-list")
        self.list_box.set_margin_start(8)
        self.list_box.set_margin_end(8)

        scrolled.set_child(self.list_box)
        self.append(scrolled)

        self.refresh()

    def refresh(self):
        # Clear existing cards
        while True:
            row = self.list_box.get_row_at_index(0)
            if row is None:
                break
            self.list_box.remove(row)

        schedule = self.scheduler.get_todays_schedule()

        if not schedule:
            empty = Gtk.Label(label=_("No medications scheduled today"))
            empty.add_css_class("dim-label")
            empty.add_css_class("title-3")
            empty.set_margin_top(48)
            self.list_box.append(empty)
            return

        for med, dose, time_str, history_entry in schedule:
            card = MedCard(med, dose, time_str, history_entry, self.pictogram_service)
            card.confirm_btn.connect("dose-confirmed", self._on_dose_confirmed, history_entry, med, dose, time_str)
            self.list_box.append(card)

    def _on_dose_confirmed(self, button, history_entry, medication, dose, time_str):
        from datetime import datetime
        if history_entry is None:
            from mediremind.models.history_entry import HistoryEntry
            today_str = datetime.now().strftime("%Y-%m-%d")
            history_entry = HistoryEntry(
                dose_id=dose.id,
                medication_id=medication.id,
                scheduled_time=f"{today_str}T{time_str}:00",
            )
            self.persistence.add_history_entry(history_entry)

        self.scheduler.confirm_dose(history_entry)
