from pydantic import BaseModel


class AIAnalysisResponse(BaseModel):
    id: int
    ticket_id: int
    category: str
    priority: str
    sentiment: str
    suggested_response: str