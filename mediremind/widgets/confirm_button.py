"""Large accessible confirmation button."""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GObject


class ConfirmButton(Gtk.Button):
    __gsignals__ = {
        "dose-confirmed": (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    def __init__(self):
        super().__init__()
        self.set_size_request(200, 80)
        self.add_css_class("confirm-button")
        self.add_css_class("suggested-action")

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_halign(Gtk.Align.CENTER)

        icon = Gtk.Image.new_from_icon_name("object-select-symbolic")
        icon.set_icon_size(Gtk.IconSize.LARGE)
        box.append(icon)

        self._label = Gtk.Label(label=_("Bekr\u00e4fta"))
        self._label.add_css_class("confirm-label")
        box.append(self._label)

        self.set_child(box)
        self.connect("clicked", self._on_clicked)
        self._confirmed = False
        self._icon = icon

    def _on_clicked(self, button):
        if not self._confirmed:
            self._confirmed = True
            self._label.set_text(_("Bekr\u00e4ftad!"))
            self._icon.set_from_icon_name("emblem-ok-symbolic")
            self.remove_css_class("suggested-action")
            self.add_css_class("success")
            self.set_sensitive(False)
            self.emit("dose-confirmed")

    def reset(self):
        self._confirmed = False
        self._label.set_text(_("Bekr\u00e4fta"))
        self._icon.set_from_icon_name("object-select-symbolic")
        self.remove_css_class("success")
        self.add_css_class("suggested-action")
        self.set_sensitive(True)
