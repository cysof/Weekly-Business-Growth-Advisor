from fastapi import FastAPI
from app.routers import insights
import app.scheduler as scheduler

app = FastAPI(title="Weekly Business Growth Advisor")

# Include routers
app.include_router(insights.router)

# Start background tasks (Scheduler)
scheduler.start()

@app.get("/")
def read_root():
    return {"message": "Weekly Business Growth Advisor is running!"}
