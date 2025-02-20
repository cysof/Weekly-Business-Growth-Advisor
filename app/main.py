from fastapi import FastAPI, BackgroundTasks
import requests
from app.models import TickPayload 
from app.services import generate_insight 
import logging

app = FastAPI(title="Weekly Business Growth Advisor")

logger = logging.getLogger(__name__)

def process_tick_task(payload: TickPayload):
    """
    This background task dynamically fetches data and generates a business insight,
    then posts the results back to Telex via the provided return_url.
    """
    try:
        # Dynamically fetch the insight using your business logic
        insight = generate_insight()  # generate_insight() should return an object with attributes: metric, observation, recommendation
        
        logger.info(f"Generated insight for {insight.metric}: {insight.observation}")
        
        # Prepare the result payload as expected by Telex
        result_payload = {
            "message": f"📊 {insight.observation}\n✅ {insight.recommendation}",
            "username": "Weekly Business Growth Advisor",
            "event_name": "Weekly Business Insight",
            "status": "success"
        }
        
        # Post the result back to Telex using the return_url provided in the payload
        response = requests.post(payload.return_url, json=result_payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Successfully posted insight to Telex. Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Error posting insight to Telex: {e}")

@app.post("/tick", status_code=202)
def tick_endpoint(payload: TickPayload, background_tasks: BackgroundTasks):
    """
    Tick endpoint that processes incoming requests from Telex.
    
    This endpoint is called on a scheduled basis by Telex.
    It delegates processing to a background task and immediately returns an acceptance response.
    """
    background_tasks.add_task(process_tick_task, payload)
    return {"status": "accepted"}
