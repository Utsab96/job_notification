import time
import random
import yagmail
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import requests

load_dotenv()

SEARCH_KEYWORDS = [
    "Backend Developer",
    "Python Developer",
    "Node.js Developer"
]

LINKEDIN_JOBS_URL = "https://www.linkedin.com/jobs/search?keywords="

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

print(EMAIL_PASSWORD)
print(EMAIL)
def human_delay(a=1, b=3):
    time.sleep(random.uniform(a, b))


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

    print("📧 Email sent successfully!")


# def fetch_jobs(playwright):
#     browser = playwright.chromium.launch_persistent_context(
#         user_data_dir=r"C:\Users\utsab\AppData\Local\Google\Chrome\User Data",
#         headless=True,
        
#     )

#     page = browser.new_page()

#     all_results = []

#     for keyword in SEARCH_KEYWORDS:
#         print(f"\nSearching for: {keyword}")
#         search_url = f"{LINKEDIN_JOBS_URL}{keyword.replace(' ', '%20')}"

#         page.goto(search_url, timeout=60000)
#         human_delay(3, 5)

#         jobs = page.locator("ul.jobs-search__results-list li").all()[:10]

#         for job in jobs:
#             try:
#                 title = job.locator("h3").inner_text().strip()
#                 company = job.locator("h4").inner_text().strip()
#                 location = job.locator(".job-search-card__location").inner_text().strip()
#                 link = job.locator("a").first.get_attribute("href")

#                 all_results.append({
#                     "title": title,
#                     "company": company,
#                     "location": location,
#                     "link": link
#                 })
#             except:
#                 continue

#     browser.close()
#     print(all_results)
#     return all_results



def fetch_jobs(keywords):
    url = "https://linkedin-jobs-api.p.rapidapi.com/jobs/search"

    payload = { "keywords": keywords }
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_KEY"),
        "X-RapidAPI-Host": "linkedin-jobs-api.p.rapidapi.com"
    }

    return requests.post(url, json=payload, headers=headers).json()
def main():
    with sync_playwright() as p:
        results = fetch_jobs(p)

        if results:
            send_email(results)
        else:
            print("No jobs found.")


if __name__ == "__main__":
    main()
