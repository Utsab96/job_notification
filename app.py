from fastapi import FastAPI
from pydantic import BaseModel
from linkedin_bot.scraper import fetch_jobs
from linkedin_bot.mailer import send_email

app = FastAPI()

class JobRequest(BaseModel):
    keywords: list[str]
    location: str
    max_days: int   # 7, 15, 30, etc.


@app.get("/render")
def home():
    return {"message": "Hello from Render!"}


@app.get("/")
def root():
    return {"message": "LinkedIn Job Bot API running!"}

@app.post("/search")
def search_jobs(data: JobRequest):
    results = fetch_jobs(data.keywords, data.location, data.max_days)
    return {"results": results}

@app.post("/send-mail")
def send_results(data: JobRequest):
    results = fetch_jobs(data.keywords, data.location, data.max_days)
    msg = send_email(results)
    return {"message": msg, "jobs_sent": len(results)}
