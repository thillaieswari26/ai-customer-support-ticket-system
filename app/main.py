from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse

app = FastAPI(title="AI Customer Support Ticket System")


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.post(
    "/tickets",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ticket(
    ticket_data: TicketCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        ticket = Ticket(
            title=ticket_data.title,
            description=ticket_data.description,
            status="OPEN",
            priority=ticket_data.priority,
            category=ticket_data.category,
            customer_id=ticket_data.customer_id,
        )

        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)

        return ticket

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to create ticket",
        )