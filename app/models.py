from pydantic import BaseModel
from typing import Optional

class BusinessInsight(BaseModel):
    metric: str
    observation: str
    recommendation: str
