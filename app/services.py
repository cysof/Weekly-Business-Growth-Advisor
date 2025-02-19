import requests
from app.models import BusinessInsight

def get_sales_data():
    # Example: Fetch from Stripe API (replace with real API call)
    return {"revenue": 5000, "previous_revenue": 7000}

def generate_insight():
    data = get_sales_data()
    
    if data["revenue"] < data["previous_revenue"]:
        return BusinessInsight(
            metric="Revenue",
            observation="Revenue dropped by 20% this week.",
            recommendation="Run a promotional discount or email campaign to re-engage customers."
        )
    else:
        return BusinessInsight(
            metric="Revenue",
            observation="Revenue is stable.",
            recommendation="Consider scaling ads for further growth."
        )
