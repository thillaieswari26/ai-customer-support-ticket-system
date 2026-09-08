from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=5)
    priority: str = "MEDIUM"
    category: str = "GENERAL"
    customer_id: int


class TicketUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=255)
    description: str | None = Field(None, min_length=5)
    status: str | None = None
    priority: str | None = None
    category: str | None = None


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    category: str

    model_config = {"from_attributes": True}