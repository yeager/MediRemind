"""Full-screen reminder overlay for medication doses."""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, GObject

from mediremind.widgets.pictogram_image import PictogramImage
from mediremind.services.pictogram import PictogramService


class ReminderView(Gtk.Window):
    """Modal reminder window with pictogram, sound, and confirm button."""

    __gsignals__ = {
        "dose-confirmed": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "dose-snoozed": (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    def __init__(self, app, medication, dose, entry):
        super().__init__(
            application=app,
            modal=True,
            title=_("Medicine reminder"),
        )
        self.medication = medication
        self.dose = dose
        self.entry = entry
        self.pictogram_service = PictogramService()

        self.set_default_size(500, 600)
        self.add_css_class("reminder-window")

        # Main container
        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
        )
        main_box.set_margin_top(32)
        main_box.set_margin_bottom(32)
        main_box.set_margin_start(32)
        main_box.set_margin_end(32)
        main_box.set_valign(Gtk.Align.CENTER)
        main_box.set_halign(Gtk.Align.CENTER)

        # Alert icon
        alert_label = Gtk.Label(label="\U0001f514")  # bell emoji
        alert_label.add_css_class("reminder-bell")
        main_box.append(alert_label)

        # Title
        title = Gtk.Label(label=_("Time for medicine!"))
        title.add_css_class("reminder-title")
        main_box.append(title)

        # Pictogram
        picto = PictogramImage(size=128)
        picto_path = self.pictogram_service.get_pictogram_path(medication)
        picto.set_from_file(picto_path)
        picto.set_halign(Gtk.Align.CENTER)
        main_box.append(picto)

        # Medication name
        name_label = Gtk.Label(label=medication.name)
        name_label.add_css_class("reminder-med-name")
        main_box.append(name_label)

        # Dosage
        dosage_label = Gtk.Label(label=dose.dosage)
        dosage_label.add_css_class("reminder-dosage")
        main_box.append(dosage_label)

        # Confirm button
        confirm_btn = Gtk.Button()
        confirm_btn.set_size_request(300, 100)
        confirm_btn.add_css_class("suggested-action")
        confirm_btn.add_css_class("confirm-button")

        confirm_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        confirm_box.set_halign(Gtk.Align.CENTER)

        icon = Gtk.Image.new_from_icon_name("object-select-symbolic")
        icon.set_icon_size(Gtk.IconSize.LARGE)
        confirm_box.append(icon)

        confirm_label = Gtk.Label(label=_("I have taken my medicine"))
        confirm_label.add_css_class("confirm-label")
        confirm_box.append(confirm_label)

        confirm_btn.set_child(confirm_box)
        confirm_btn.connect("clicked", self._on_confirm)
        main_box.append(confirm_btn)

        # Snooze button
        snooze_btn = Gtk.Button(label=_("Remind me in 5 minutes"))
        snooze_btn.add_css_class("snooze-button")
        snooze_btn.set_size_request(300, 60)
        snooze_btn.connect("clicked", self._on_snooze)
        main_box.append(snooze_btn)

        self.set_child(main_box)

    def _on_confirm(self, button):
        self.emit("dose-confirmed")
        self.close()

    def _on_snooze(self, button):
        self.emit("dose-snoozed")
        self.close()
