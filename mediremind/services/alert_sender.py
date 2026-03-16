"""Alert sender for missed doses via email and SMS."""

import smtplib
import urllib.request
import urllib.parse
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class AlertSender:
    def __init__(self, settings):
        self.settings = settings

    def send_missed_alert(self, medication, scheduled_time):
        contact_email = self.settings.get("contact_email", "")
        contact_phone = self.settings.get("contact_phone", "")
        contact_name = self.settings.get("contact_name", "anh\u00f6rig")

        message = _(
            "Hello {contact}! {med_name} (scheduled {time}) has not been confirmed. "
            "V\u00e4nligen kontrollera att medicinen har tagits."
        ).format(contact=contact_name, med_name=medication.name, time=scheduled_time)

        success = False
        if contact_email:
            try:
                self._send_email(contact_email, message, medication.name)
                success = True
            except Exception as e:
                print(f"E-post misslyckades: {e}")
        if contact_phone:
            try:
                self._send_sms(contact_phone, message)
                success = True
            except Exception as e:
                print(f"SMS misslyckades: {e}")
        return success

    def _send_email(self, to_email, message, med_name):
        smtp_server = self.settings.get("smtp_server", "")
        smtp_port = self.settings.get("smtp_port", 587)
        smtp_user = self.settings.get("smtp_user", "")
        smtp_password = self.settings.get("smtp_password", "")
        if not smtp_server or not smtp_user:
            return

        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = _("MediRemind: Missed dose - {name}").format(name=med_name)
        msg.attach(MIMEText(message, "plain", "utf-8"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())

    def _send_sms(self, phone, message):
        api_key = self.settings.get("sms_api_key", "")
        api_url = self.settings.get("sms_api_url", "")
        if not api_key or not api_url:
            return

        data = urllib.parse.urlencode({"to": phone, "message": message}).encode("utf-8")
        req = urllib.request.Request(api_url, data=data)
        req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
