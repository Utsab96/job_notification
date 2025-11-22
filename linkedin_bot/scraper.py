from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
from .utils import human_delay

load_dotenv()

LOCATION = os.getenv("LOCATION")
LINKEDIN_URL = "https://www.linkedin.com/jobs/search?keywords="

def fetch_jobs(keywords):

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=r"C:\Users\utsab\AppData\Local\Google\Chrome\User Data",
            headless=True   # make backend-friendly
        )

        page = browser.new_page()
        all_results = []

        for keyword in keywords:
            # include location
            search_url = f"{LINKEDIN_URL}{keyword.replace(' ', '%20')}&location={LOCATION.replace(' ', '%20')}"
            print("Searching:", search_url)

            page.goto(search_url)
            human_delay(3, 5)

            jobs = page.locator("ul.jobs-search__results-list li").all()[:10]

            for job in jobs:
                try:
                    title = job.locator("h3").inner_text().strip()
                    company = job.locator("h4").inner_text().strip()
                    location = job.locator(".job-search-card__location").inner_text().strip()
                    link = job.locator("a").first.get_attribute("href")

                    all_results.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "link": link
                    })
                except:
                    continue

        browser.close()
        return all_results
