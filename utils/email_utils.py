import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY


def send_resend_email(to_email, subject, html_content, from_email="YourApp <noreply@yourdomain.com>"):
    try:
        params = {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_content
        }

        response = resend.Emails.send(params)
        return response
    except Exception as e:
        return {"error": str(e)}
