"""History view showing past dose confirmations."""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from datetime import datetime, timedelta


class HistoryView(Gtk.Box):
    """Log of taken/missed doses for the past 7 days."""

    def __init__(self, persistence):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.persistence = persistence

        header = Gtk.Label(label=_("History"))
        header.add_css_class("title-1")
        header.set_halign(Gtk.Align.START)
        header.set_margin_top(16)
        header.set_margin_bottom(8)
        header.set_margin_start(16)
        self.append(header)

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
        while True:
            row = self.list_box.get_row_at_index(0)
            if row is None:
                break
            self.list_box.remove(row)

        now = datetime.now()
        week_ago = (now - timedelta(days=7)).isoformat()

        recent = [
            h for h in self.persistence.history
            if h.scheduled_time >= week_ago
        ]
        recent.sort(key=lambda h: h.scheduled_time, reverse=True)

        if not recent:
            empty = Gtk.Label(label=_("No history yet"))
            empty.add_css_class("dim-label")
            empty.set_margin_top(48)
            self.list_box.append(empty)
            return

        for entry in recent:
            row = self._create_row(entry)
            self.list_box.append(row)

    def _create_row(self, entry):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(8)
        box.set_margin_bottom(8)

        if entry.status == "taken":
            icon = Gtk.Label(label="\u2705")
        elif entry.status == "missed":
            icon = Gtk.Label(label="\u274c")
        else:
            icon = Gtk.Label(label="\u23f0")
        icon.set_size_request(32, 32)
        box.append(icon)

        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        info_box.set_hexpand(True)

        med = self.persistence.get_medication_by_id(entry.medication_id)
        name = med.name if med else _("Unknown medicine")
        name_label = Gtk.Label(label=name)
        name_label.set_halign(Gtk.Align.START)
        name_label.add_css_class("heading")
        info_box.append(name_label)

        try:
            dt = datetime.fromisoformat(entry.scheduled_time)
            time_text = dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            time_text = entry.scheduled_time
        time_label = Gtk.Label(label=time_text)
        time_label.set_halign(Gtk.Align.START)
        time_label.add_css_class("dim-label")
        info_box.append(time_label)

        box.append(info_box)

        status_map = {
            "taken": _("Tagen"),
            "missed": _("Missad"),
            "pending": _("Waiting"),
            "snoozed": _("Snoozad"),
        }
        status_label = Gtk.Label(label=status_map.get(entry.status, entry.status))
        status_label.add_css_class(f"status-{entry.status}")
        box.append(status_label)

        return box
