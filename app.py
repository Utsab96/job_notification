from fastapi import FastAPI
from pydantic import BaseModel
from linkedin_bot.scraper import fetch_jobs
from linkedin_bot.mailer import send_email

app = FastAPI()

class JobRequest(BaseModel):
    keywords: list[str]


@app.route("/render")
def home():
    return "Hello from Render!"

@app.get("/")
def root():
    return {"message": "LinkedIn Job Bot API running!"}

@app.post("/search")
def search_jobs(data: JobRequest):
    results = fetch_jobs(data.keywords)
    return {"results": results}

@app.post("/send-mail")
def send_results(data: JobRequest):
    results = fetch_jobs(data.keywords)
    msg = send_email(results)
    return {"message": msg, "jobs_sent": len(results)}
