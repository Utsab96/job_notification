from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import urllib.parse
from .utils import human_delay, parse_days_ago

load_dotenv()

LOCATION = os.getenv("LOCATION")
LINKEDIN_URL = "https://www.linkedin.com/jobs/search?keywords="

def fetch_jobs(keywords, location, max_days):
    all_results = []
    encoded_location = urllib.parse.quote(location)

    for keyword in keywords:
        encoded_keyword = urllib.parse.quote(keyword)

        url = (
            f"https://www.linkedin.com/jobs-guest/jobs/api/"
            f"seeMoreJobPostings/search?keywords={encoded_keyword}&location={encoded_location}"
        )

        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")

        for job in soup.select("li"):
            try:
                title = job.select_one(".base-search-card__title").get_text(strip=True)
                company = job.select_one(".base-search-card__subtitle").get_text(strip=True)
                loc = job.select_one(".job-search-card__location").get_text(strip=True)
                link = job.select_one("a")["href"]

                date_text = job.select_one("time").get_text(strip=True)
                days_ago = parse_days_ago(date_text)

                # ⭐ Dynamic filter
                if days_ago <= max_days:
                    all_results.append({
                        "title": title,
                        "company": company,
                        "location": loc,
                        "link": link,
                        "posted": date_text,
                        "days_ago": days_ago
                    })

            except:
                continue

    return all_results