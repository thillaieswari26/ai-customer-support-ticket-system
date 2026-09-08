from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import select
from app.db.database import AsyncSessionLocal
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate

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
@app.get("/tickets", response_model=list[TicketResponse])
async def list_tickets(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Ticket)
        .order_by(Ticket.id.asc())
        .offset(skip)
        .limit(limit)
    )

    return result.scalars().all()


@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Ticket).where(Ticket.id == ticket_id)
    )

    ticket = result.scalar_one_or_none()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket
@app.put("/tickets/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Ticket).where(Ticket.id == ticket_id)
    )

    ticket = result.scalar_one_or_none()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    update_data = ticket_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(ticket, field, value)

    try:
        await db.commit()
        await db.refresh(ticket)
        return ticket

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to update ticket",
        )


@app.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Ticket).where(Ticket.id == ticket_id)
    )

    ticket = result.scalar_one_or_none()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    try:
        await db.delete(ticket)
        await db.commit()

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to delete ticket",
        )