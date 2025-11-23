import requests
import resend
import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
resend.api_key = os.getenv("RESEND_API_KEY")

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

#     return "Email sent successfully!"


def send_email(results):
    body = "\n\n".join([
        f"🔹 {job['title']}\n{job['company']}\n{job['location']}\n{job['link']}"
        for job in results
    ])

    r = resend.Emails.send({
        "from": "Utsab <onboarding@resend.dev>",
        "to": ["utsab.ghosh96@gmail.com"],
        "subject": "LinkedIn Job Updates",
        "text": body
    })

    return r