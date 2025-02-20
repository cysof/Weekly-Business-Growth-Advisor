from fastapi import FastAPI
from app.routers import insights
import app.scheduler as scheduler
from fastapi import HTTPException

app = FastAPI(title="Weekly Business Growth Advisor")

# Include routers
app.include_router(insights.router)

# Start background tasks (Scheduler)
scheduler.start()

@app.get("/")
def read_root():
    """
    Root endpoint for the FastAPI application.

    Returns:
        dict: A message indicating the status of the Weekly Business Growth Advisor.
    """

    return {"message": "Weekly Business Growth Advisor is running!"}




# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)