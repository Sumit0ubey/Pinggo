from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
import requests


class MailAPIXBackend(BaseEmailBackend):

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        sent = 0
        for msg in email_messages:
            to_list = list(msg.to or [])
            if not to_list:
                continue

            text_body = msg.body or ""

            html_body = None
            if getattr(msg, "alternatives", None):
                for content, mimetype in msg.alternatives:
                    if mimetype == "text/html":
                        html_body = content
                        break

            payload = {
                "title": msg.subject or "",
                "content": text_body,
                "sendTo": to_list if len(to_list) > 1 else to_list[0],
                "passKey": settings.EMAIL_HOST_PASSWORD,
                "customHtml": html_body,
            }

            try:
                r = requests.post(
                    f"{settings.MAILAPIX_BASE_URL.rstrip('/')}/email?email_title={msg.subject}&template_id=4",
                    json=payload,
                    headers={"token": settings.MAILAPIX_TOKEN},
                    timeout=20,
                )
                if r.status_code >= 400:
                    if self.fail_silently:
                        continue
                    raise Exception(f"MailAPIX error {r.status_code}: {r.text}")
                sent += 1
            except Exception:
                if not self.fail_silently:
                    raise

        return sent
