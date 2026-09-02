from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    description: str


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    category: str
class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    category: str | None = None
    assigned_agent_id: int | None = None