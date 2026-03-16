"""Medication card widget for the schedule list."""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from mediremind.widgets.pictogram_image import PictogramImage
from mediremind.widgets.confirm_button import ConfirmButton


class MedCard(Gtk.Box):
    def __init__(self, medication, dose, time_str, history_entry, pictogram_service):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.medication = medication
        self.dose = dose
        self.time_str = time_str
        self.history_entry = history_entry

        self.add_css_class("med-card")
        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_margin_top(8)
        self.set_margin_bottom(8)

        # Status indicator
        status_bar = Gtk.Box()
        status_bar.set_size_request(8, -1)
        if history_entry and history_entry.status == "taken":
            status_bar.add_css_class("status-taken")
        elif history_entry and history_entry.status == "missed":
            status_bar.add_css_class("status-missed")
        else:
            from datetime import datetime
            now = datetime.now().strftime("%H:%M")
            if time_str < now and (not history_entry or history_entry.status == "pending"):
                status_bar.add_css_class("status-overdue")
            else:
                status_bar.add_css_class("status-upcoming")
        self.append(status_bar)

        # Pictogram
        picto = PictogramImage(size=96)
        picto_path = pictogram_service.get_pictogram_path(medication)
        picto.set_from_file(picto_path)
        self.append(picto)

        # Info column
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info_box.set_hexpand(True)
        info_box.set_valign(Gtk.Align.CENTER)

        name_label = Gtk.Label(label=medication.name)
        name_label.set_halign(Gtk.Align.START)
        name_label.add_css_class("med-name")
        info_box.append(name_label)

        time_label = Gtk.Label(label=f"\U0001f552 {time_str}")
        time_label.set_halign(Gtk.Align.START)
        time_label.add_css_class("med-time")
        info_box.append(time_label)

        dosage_label = Gtk.Label(label=dose.dosage)
        dosage_label.set_halign(Gtk.Align.START)
        dosage_label.add_css_class("med-dosage")
        info_box.append(dosage_label)

        self.append(info_box)

        # Confirm button
        self.confirm_btn = ConfirmButton()
        self.confirm_btn.set_valign(Gtk.Align.CENTER)
        self.append(self.confirm_btn)

        if history_entry and history_entry.status == "taken":
            self.confirm_btn._on_clicked(None)

        self.update_property(
            [Gtk.AccessibleProperty.LABEL],
            [f"{medication.name}, {time_str}, {dose.dosage}"],
        )
