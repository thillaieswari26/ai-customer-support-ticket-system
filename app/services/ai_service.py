class AIServiceError(Exception):
    """Raised when the AI service cannot complete the request."""


async def analyze_ticket(title: str, description: str) -> dict:
    """
    Local mock AI service used for development and testing.

    This keeps AI logic behind a service-layer boundary so the
    implementation can later be replaced with a real AI provider.
    """

    text = f"{title} {description}".lower()

    if any(word in text for word in ["payment", "bill", "refund", "charge"]):
        category = "BILLING"
    elif any(word in text for word in ["login", "password", "error", "bug", "crash"]):
        category = "TECHNICAL"
    elif any(word in text for word in ["account", "profile"]):
        category = "ACCOUNT"
    else:
        category = "GENERAL"

    if any(word in text for word in ["urgent", "failed", "blocked", "cannot"]):
        priority = "HIGH"
    elif any(word in text for word in ["problem", "issue"]):
        priority = "MEDIUM"
    else:
        priority = "LOW"

    if any(word in text for word in ["thank", "great", "happy"]):
        sentiment = "POSITIVE"
    elif any(word in text for word in ["angry", "bad", "frustrated", "disappointed"]):
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    suggested_response = (
        "Thank you for contacting support. "
        "We have received your ticket and will review the issue shortly."
    )

    return {
        "category": category,
        "priority": priority,
        "sentiment": sentiment,
        "suggested_response": suggested_response,
    }