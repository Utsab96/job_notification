import requests
import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
BREVO_API_KEY = os.getenv("BREVO_API_KEY")

def send_email(results):
    yag = yagmail.SMTP(EMAIL, EMAIL_PASSWORD)

    body = "\n\n".join([
        f"🔹 {job['title']}\n{job['company']}\n{job['location']}\n{job['link']}"
        for job in results
    ])

    yag.send(
        to=EMAIL,
        subject="LinkedIn Job Updates",
        contents=body
    )

    return "Email sent successfully!"


