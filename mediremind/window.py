"""Main application window."""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk

from mediremind import _
from mediremind import store


class MediRemindWindow(Adw.ApplicationWindow):
    def __init__(self, app, reminder_manager):
        super().__init__(application=app, title="MediRemind", default_width=400, default_height=500)
        self.reminder = reminder_manager
        self.medications = store.load()
        self.reminder.update(self.medications)

        # Layout
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(box)

        # Header bar
        header = Adw.HeaderBar()
        add_btn = Gtk.Button(icon_name="list-add-symbolic", tooltip_text=_("Add Medication"))
        add_btn.connect("clicked", self._on_add_clicked)
        header.pack_start(add_btn)
        box.append(header)

        # Status page for empty state / list
        self.stack = Gtk.Stack()
        box.append(self.stack)

        # Empty state
        status = Adw.StatusPage(
            title=_("No Medications"),
            description=_("Click + to add your first medication"),
            icon_name="medication-symbolic",
        )
        self.stack.add_named(status, "empty")

        # List view
        scrolled = Gtk.ScrolledWindow(vexpand=True)
        self.listbox = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        self.listbox.add_css_class("boxed-list")
        self.listbox.set_margin_start(12)
        self.listbox.set_margin_end(12)
        self.listbox.set_margin_top(12)
        self.listbox.set_margin_bottom(12)
        scrolled.set_child(self.listbox)
        self.stack.add_named(scrolled, "list")

        self._rebuild_list()

    def _rebuild_list(self):
        while row := self.listbox.get_row_at_index(0):
            self.listbox.remove(row)

        if not self.medications:
            self.stack.set_visible_child_name("empty")
            return

        self.stack.set_visible_child_name("list")
        for i, med in enumerate(self.medications):
            row = Adw.ActionRow(title=med["name"], subtitle=med["time"])
            delete_btn = Gtk.Button(icon_name="user-trash-symbolic", valign=Gtk.Align.CENTER)
            delete_btn.add_css_class("flat")
            delete_btn.connect("clicked", self._on_delete_clicked, i)
            row.add_suffix(delete_btn)
            self.listbox.append(row)

    def _on_delete_clicked(self, _btn, index):
        del self.medications[index]
        store.save(self.medications)
        self.reminder.update(self.medications)
        self._rebuild_list()

    def _on_add_clicked(self, _btn):
        dialog = Adw.AlertDialog(heading=_("Add Medication"))
        dialog.set_body(_("Enter medication name and time (HH:MM)"))

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        content.set_margin_start(12)
        content.set_margin_end(12)

        self.name_entry = Gtk.Entry(placeholder_text=_("Medication name"))
        self.time_entry = Gtk.Entry(placeholder_text="08:00")
        self.error_label = Gtk.Label(label="", css_classes=["error"])
        self.error_label.set_visible(False)

        content.append(self.name_entry)
        content.append(self.time_entry)
        content.append(self.error_label)
        dialog.set_extra_child(content)

        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("add", _("Add"))
        dialog.set_response_appearance("add", Adw.ResponseAppearance.SUGGESTED)
        dialog.connect("response", self._on_add_response)
        dialog.present(self)

    def _on_add_response(self, dialog, response):
        if response != "add":
            return
        name = self.name_entry.get_text().strip()
        time = self.time_entry.get_text().strip()
        error = store.validate(name, time)
        if error:
            self.error_label.set_label(error)
            self.error_label.set_visible(True)
            return
        self.medications.append({"name": name, "time": time})
        self.medications.sort(key=lambda m: m["time"])
        store.save(self.medications)
        self.reminder.update(self.medications)
        self._rebuild_list()
