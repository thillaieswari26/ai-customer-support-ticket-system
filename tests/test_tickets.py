import pytest

from app.models.user import User
from app.core.security import get_password_hash, create_access_token
from app.services import ai_service


async def create_test_user(db_session, email):
    user = User(
        name="Test User",
        email=email,
        password=get_password_hash("test-password"),
        role="CUSTOMER",
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


async def create_test_ticket(client, token):
    response = await client.post(
        "/tickets",
        json={
            "title": "Test ticket",
            "description": "This is a test ticket",
            "priority": "MEDIUM",
            "category": "GENERAL",
            "customer_id": 1,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 201
    return response


@pytest.mark.asyncio
async def test_create_ticket(client, db_session):
    user = await create_test_user(
        db_session,
        "test-create@example.com",
    )

    token = create_access_token({"sub": str(user.id)})

    response = await client.post(
        "/tickets",
        json={
            "title": "Test ticket",
            "description": "This is a test ticket",
            "priority": "MEDIUM",
            "category": "GENERAL",
            "customer_id": user.id,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test ticket"
    assert data["description"] == "This is a test ticket"


@pytest.mark.asyncio
async def test_create_ticket_validation_failure(client, db_session):
    user = await create_test_user(
        db_session,
        "validation@example.com",
    )

    token = create_access_token({"sub": str(user.id)})

    response = await client.post(
        "/tickets",
        json={
            "title": "",
            "description": "Invalid ticket",
            "priority": "MEDIUM",
            "category": "GENERAL",
            "customer_id": user.id,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_tickets(client, db_session):
    user = await create_test_user(
        db_session,
        "list@example.com",
    )

    token = create_access_token({"sub": str(user.id)})

    await create_test_ticket(client, token)

    response = await client.get(
        "/tickets",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_ticket(client, db_session):
    user = await create_test_user(
        db_session,
        "detail@example.com",
    )

    token = create_access_token({"sub": str(user.id)})

    create_response = await create_test_ticket(client, token)
    ticket_id = create_response.json()["id"]

    response = await client.get(
        f"/tickets/{ticket_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == ticket_id


@pytest.mark.asyncio
async def test_update_ticket(client, db_session):
    user = await create_test_user(
        db_session,
        "update@example.com",
    )

    token = create_access_token({"sub": str(user.id)})

    create_response = await create_test_ticket(client, token)
    ticket_id = create_response.json()["id"]

    response = await client.put(
        f"/tickets/{ticket_id}",
        json={
            "title": "Updated ticket",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated ticket"


@pytest.mark.asyncio
async def test_delete_ticket(client, db_session):
    user = await create_test_user(
        db_session,
        "delete@example.com",
    )

    token = create_access_token({"sub": str(user.id)})

    create_response = await create_test_ticket(client, token)
    ticket_id = create_response.json()["id"]

    response = await client.delete(
        f"/tickets/{ticket_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_user_cannot_access_another_users_ticket(client, db_session):
    user_a = await create_test_user(
        db_session,
        "user-a@example.com",
    )

    user_b = await create_test_user(
        db_session,
        "user-b@example.com",
    )

    token_a = create_access_token({"sub": str(user_a.id)})
    token_b = create_access_token({"sub": str(user_b.id)})

    create_response = await client.post(
        "/tickets",
        json={
            "title": "Private ticket",
            "description": "This belongs to User A",
            "priority": "MEDIUM",
            "category": "GENERAL",
            "customer_id": user_a.id,
        },
        headers={
            "Authorization": f"Bearer {token_a}"
        },
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.get(
        f"/tickets/{ticket_id}",
        headers={
            "Authorization": f"Bearer {token_b}"
        },
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_ai_service_failure(client, db_session, monkeypatch):
    user = await create_test_user(
        db_session,
        "ai-failure@example.com",
    )

    token = create_access_token({"sub": str(user.id)})

    create_response = await create_test_ticket(client, token)
    ticket_id = create_response.json()["id"]

    async def mock_ai_failure(title, description):
        raise ai_service.AIServiceError("AI service unavailable")

    monkeypatch.setattr(
        ai_service,
        "analyze_ticket",
        mock_ai_failure,
    )

    response = await client.post(
        f"/tickets/{ticket_id}/analyze",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "AI service unavailable"