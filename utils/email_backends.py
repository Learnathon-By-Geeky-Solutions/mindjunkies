from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from django.core.mail import EmailMessage
import resend


class ResendEmailBackend(BaseEmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        resend.api_key = settings.RESEND_API_KEY

    def send_messages(self, email_messages):
        sent_count = 0
        for message in email_messages:
            try:
                # Fallback if 'from_email' is not set on message
                from_email = message.from_email or settings.DEFAULT_FROM_EMAIL

                resend.Emails.send({
                    "from": from_email,
                    "to": message.to,
                    "subject": message.subject,
                    "html": message.alternatives[0][0] if message.alternatives else message.body,
                })
                sent_count += 1
            except Exception as e:
                if not self.fail_silently:
                    raise e
        return sent_count
