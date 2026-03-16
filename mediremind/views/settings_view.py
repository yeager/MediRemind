"""Settings view for contacts, notifications, and medication management."""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk

from mediremind.models.medication import Medication
from mediremind.models.dose import DoseSchedule


class SettingsView(Gtk.Box):
    """Settings page with contact info, preferences, and medication management."""

    def __init__(self, persistence, on_schedule_changed=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.persistence = persistence
        self.on_schedule_changed = on_schedule_changed

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        content.set_margin_top(16)
        content.set_margin_bottom(16)
        content.set_margin_start(16)
        content.set_margin_end(16)

        # Title
        title = Gtk.Label(label=_("Settings"))
        title.add_css_class("title-1")
        title.set_halign(Gtk.Align.START)
        content.append(title)

        # Contact section
        contact_frame = self._create_section(_("Anhörigkontakt"))
        self.contact_name = self._add_entry(contact_frame, _("Name"), "contact_name")
        self.contact_email = self._add_entry(contact_frame, _("E-post"), "contact_email")
        self.contact_phone = self._add_entry(contact_frame, _("Telefon"), "contact_phone")
        content.append(contact_frame)

        # Email settings
        email_frame = self._create_section(_("E-postinställningar (SMTP)"))
        self.smtp_server = self._add_entry(email_frame, _("SMTP-server"), "smtp_server")
        self.smtp_user = self._add_entry(email_frame, _("Användare"), "smtp_user")
        self.smtp_password = self._add_entry(email_frame, _("Lösenord"), "smtp_password", password=True)
        content.append(email_frame)

        # Notification settings
        notif_frame = self._create_section(_("Notifieringar"))
        self.missed_timeout = self._add_entry(
            notif_frame, _("Time innan varning (minuter)"), "missed_timeout_minutes"
        )
        content.append(notif_frame)

        # Medication management
        med_frame = self._create_section(_("Mediciner"))
        self.med_list = Gtk.ListBox()
        self.med_list.set_selection_mode(Gtk.SelectionMode.NONE)
        self.med_list.add_css_class("boxed-list")
        med_frame.append(self.med_list)

        add_btn = Gtk.Button(label=_("Add medicin"))
        add_btn.add_css_class("suggested-action")
        add_btn.set_margin_top(8)
        add_btn.connect("clicked", self._on_add_medication)
        med_frame.append(add_btn)

        content.append(med_frame)

        # Save button
        save_btn = Gtk.Button(label=_("Save inställningar"))
        save_btn.add_css_class("suggested-action")
        save_btn.set_size_request(-1, 60)
        save_btn.connect("clicked", self._on_save)
        content.append(save_btn)

        scrolled.set_child(content)
        self.append(scrolled)

        self._refresh_med_list()

    def _create_section(self, title):
        frame = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        label = Gtk.Label(label=title)
        label.add_css_class("title-3")
        label.set_halign(Gtk.Align.START)
        frame.append(label)
        return frame

    def _add_entry(self, parent, label_text, setting_key, password=False):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_top(4)

        label = Gtk.Label(label=label_text)
        label.set_size_request(200, -1)
        label.set_halign(Gtk.Align.START)
        box.append(label)

        entry = Gtk.Entry()
        entry.set_hexpand(True)
        if password:
            entry.set_visibility(False)

        value = self.persistence.settings.get(setting_key, "")
        entry.set_text(str(value))
        entry.setting_key = setting_key
        box.append(entry)

        parent.append(box)
        return entry

    def _refresh_med_list(self):
        while True:
            row = self.med_list.get_row_at_index(0)
            if row is None:
                break
            self.med_list.remove(row)

        for med in self.persistence.medications:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            row.set_margin_start(8)
            row.set_margin_end(8)
            row.set_margin_top(4)
            row.set_margin_bottom(4)

            name_label = Gtk.Label(label=med.name)
            name_label.set_hexpand(True)
            name_label.set_halign(Gtk.Align.START)
            row.append(name_label)

            form_label = Gtk.Label(label=med.form)
            form_label.add_css_class("dim-label")
            row.append(form_label)

            del_btn = Gtk.Button.new_from_icon_name("user-trash-symbolic")
            del_btn.add_css_class("destructive-action")
            del_btn.connect("clicked", self._on_delete_medication, med)
            row.append(del_btn)

            self.med_list.append(row)

    def _on_add_medication(self, button):
        dialog = AddMedicationDialog(self.get_root())
        dialog.connect("response", self._on_add_dialog_response)
        dialog.present()

    def _on_add_dialog_response(self, dialog, response):
        if response == "add":
            name = dialog.name_entry.get_text().strip()
            if not name:
                return
            form = dialog.form_combo.get_active_id() or "pill"
            dosage = dialog.dosage_entry.get_text().strip() or "1 tablett"
            times_text = dialog.times_entry.get_text().strip() or "08:00"
            times = [t.strip() for t in times_text.split(",")]

            med = Medication(name=name, form=form)
            self.persistence.medications.append(med)

            dose = DoseSchedule(
                medication_id=med.id,
                times=times,
                dosage=dosage,
            )
            self.persistence.doses.append(dose)
            self.persistence.save_schedule()

            self._refresh_med_list()
            if self.on_schedule_changed:
                self.on_schedule_changed()

        dialog.close()

    def _on_delete_medication(self, button, medication):
        self.persistence.medications = [
            m for m in self.persistence.medications if m.id != medication.id
        ]
        self.persistence.doses = [
            d for d in self.persistence.doses if d.medication_id != medication.id
        ]
        self.persistence.save_schedule()
        self._refresh_med_list()
        if self.on_schedule_changed:
            self.on_schedule_changed()

    def _on_save(self, button):
        for entry in [
            self.contact_name, self.contact_email, self.contact_phone,
            self.smtp_server, self.smtp_user, self.smtp_password,
            self.missed_timeout,
        ]:
            key = entry.setting_key
            value = entry.get_text()
            if key == "missed_timeout_minutes":
                try:
                    value = int(value)
                except ValueError:
                    value = 30
            self.persistence.settings[key] = value
        self.persistence.save_settings()


class AddMedicationDialog(Gtk.Dialog):
    """Dialog for adding a new medication."""

    def __init__(self, parent):
        super().__init__(
            title=_("Add medicin"),
            transient_for=parent,
            modal=True,
        )
        self.add_button(_("Cancel"), "cancel")
        self.add_button(_("Add"), "add")

        content = self.get_content_area()
        content.set_spacing(12)
        content.set_margin_top(16)
        content.set_margin_bottom(16)
        content.set_margin_start(16)
        content.set_margin_end(16)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text(_("Medicinnamn"))
        content.append(self.name_entry)

        self.form_combo = Gtk.ComboBoxText()
        for form_id, label in [
            ("pill", _("Tablett")),
            ("injection", _("Injektion")),
            ("drops", _("Droppar")),
            ("inhaler", _("Inhalator")),
            ("ointment", _("Salva")),
        ]:
            self.form_combo.append(form_id, label)
        self.form_combo.set_active_id("pill")
        content.append(self.form_combo)

        self.dosage_entry = Gtk.Entry()
        self.dosage_entry.set_placeholder_text(_("Dosering, t.ex. 2 tabletter"))
        content.append(self.dosage_entry)

        self.times_entry = Gtk.Entry()
        self.times_entry.set_placeholder_text(_("Tider, t.ex. 08:00, 20:00"))
        content.append(self.times_entry)
