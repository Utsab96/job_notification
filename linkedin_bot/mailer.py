import requests
import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
BREVO_API_KEY = os.getenv("BREVO_API_KEY")

# def send_email(results):
#     yag = yagmail.SMTP(EMAIL, EMAIL_PASSWORD)

#     body = "\n\n".join([
#         f"🔹 {job['title']}\n{job['company']}\n{job['location']}\n{job['link']}"
#         for job in results
#     ])

#     yag.send(
#         to=EMAIL,
#         subject="LinkedIn Job Updates",
#         contents=body
#     )

    # return "Email sent successfully!"


def send_email(results):

    if not results:
        return "No jobs found to send."

    body_html = "<br><br>".join([
        f"<strong>{job['title']}</strong><br>"
        f"{job['company']}<br>"
        f"{job['location']}<br>"
        f"<a href='{job['link']}'>Apply Here</a>"
        for job in results
    ])

    payload = {
        "sender": {"name": "Job Bot", "email": EMAIL},
        "to": [{"email": EMAIL}],
        "subject": "LinkedIn Job Updates",
        "htmlContent": body_html
    }

    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }

    r = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers=headers,
        json=payload
    )

    if r.status_code in (200, 201):
        return "Email sent successfully!"
    else:
        return f"Failed: {r.text}"
