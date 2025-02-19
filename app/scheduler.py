from apscheduler.schedulers.background import BackgroundScheduler
import app.services as services
import requests

TELEX_WEBHOOK_URL = "https://ping.telex.im/v1/webhooks/01951969-ccbf-7ff0-be62-0c6286b0a6b7"

scheduler = BackgroundScheduler()

def send_weekly_insight():
    insight = services.generate_insight()
    payload = {"text": f"📊 {insight.observation}\n✅ {insight.recommendation}"}
    requests.post(TELEX_WEBHOOK_URL, json=payload)

def start():
    scheduler.add_job(send_weekly_insight, "cron", day_of_week="mon", hour=9)
    scheduler.start()
