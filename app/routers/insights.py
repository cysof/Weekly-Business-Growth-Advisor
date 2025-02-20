from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging
from  app.services import generate_insight

# Set up logging
logger = logging.getLogger(__name__)

# Define response models for better API documentation
class BusinessInsightResponse(BaseModel):
    metric: str
    observation: str
    recommendation: str
    generated_at: datetime

# Create router with tags and prefix
router = APIRouter(prefix="/insights", tags=["Insights"])

@router.get(
    "/",
    response_model=BusinessInsightResponse,
    summary="Get weekly business insight",
    response_description="Returns the current business insight based on latest data"
)
async def get_weekly_insight(
    response: Response
):
    """
    Returns a weekly business growth insight based on the latest sales data.
    
    The insight contains analysis of recent performance metrics and actionable
    recommendations for business growth.
    
    Returns:
        BusinessInsightResponse: An object with:
            - metric: The metric being observed (e.g. Revenue)
            - observation: Analysis of the current trend
            - recommendation: Suggested action based on the analysis
            - generated_at: Timestamp when the insight was generated
    
    Raises:
        HTTPException: 
            - 500 if insight generation fails
    """
    try:
        # Log the request
        logger.info("Generating insight")
        
        # Generate the insight
        insight = generate_insight()
        
        # Add cache control headers
        response.headers["Cache-Control"] = "max-age=3600"  # Cache for 1 hour
        
        # Return with timestamp
        return {
            "metric": insight.metric,
            "observation": insight.observation,
            "recommendation": insight.recommendation,
            "generated_at": datetime.now()
        }
    except Exception as e:
        logger.error(f"Failed to generate insight: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate business insight. Please try again later."
        )

# Additional endpoints could be added here

@router.get(
    "/metrics/{metric_name}",
    response_model=BusinessInsightResponse,
    summary="Get insight for specific metric"
)
async def get_metric_insight(
    metric_name: str
):
    """
    Returns a business insight for a specific metric.
    
    Currently supported metrics: 'revenue', 'customers', 'conversion'
    
    Returns:
        BusinessInsightResponse: Insight for the requested metric
    
    Raises:
        HTTPException: 
            - 404 if metric is not supported
    """
    # This is a placeholder - you would need to modify your generate_insight service
    # to support specific metrics
    if metric_name.lower() not in ['revenue', 'customers', 'conversion']:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Metric '{metric_name}' not supported"
        )
    
    insight = generate_insight()
    
    return {
        "metric": insight.metric,
        "observation": insight.observation,
        "recommendation": insight.recommendation,
        "generated_at": datetime.now()
    }