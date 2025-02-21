from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.config import settings

router = APIRouter()

{
  "data": {
    "date": {
      "created_at": "2025-02-20",
      "updated_at": "2025-02-20"
    },
    "descriptions": {
      "app_name": "Weekly-Business-Growth-Advisor",
      "app_description": "Provides weekly business insights based on Google Analytics data.",
      "app_logo": "https://weekly-business-growth-advisor.onrender.com",
      "app_url": "https://weekly-business-growth-advisor.onrender.com",
      "background_color": "#fff"
    },
    "is_active": True,
    "integration_type": "interval",
    "key_features": [
      "📊 Automated Business Insights – Provides weekly analytics-driven insights to improve decision-making.\n🔍 Google Analytics Integration – Uses Google Analytics data to track website performance.\n⏳ Scheduled Reports – Runs automatically every Monday at 9 AM to deliver fresh insights.\n📢 Actionable Recommendations – Offers data-driven suggestions to boost engagement and conversions.\n🚀 Telex Integration – Sends insights directly to your Telex channels for seamless notifications."
    ],
    "author": "cysoft",
    "settings": [
      {
        "label": "time interval",
        "type": "dropdown",
        "required": True,
        "default": "0 9 * * MON",
        "options": [
          "0 9 * * MON",
          "immediate",
          "Every5-min",
          "Every1-hour"
        ]
      },
      {
        "label": "Google Analytics API Key",
        "type": "text",
        "required": True,
        "default": "https://analyticsdata.googleapis.com"
      }
    ],
    "target_url": settings.TARGET_URL,
    "tick_url": settings.Tick_URL
  }
}

@router.get("/integration-config")
async def get_integration_config():
    return JSONResponse(content=integration_json)