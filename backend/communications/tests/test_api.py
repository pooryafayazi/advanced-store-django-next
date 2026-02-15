# backend\communications\tests\test_api.py
import pytest
from rest_framework.test import APIClient

from communications.models import ContactMessage, NewsletterSubscriber


CONTACT_URL = "/api/communications/contact/"
NEWSLETTER_SUB_URL = "/api/communications/newsletter/subscribe/"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_contact_create_success(api_client):
    payload = {
        "full_name": "Test User",
        "email": "test@example.com",
        "subject": "Hello",
        "message": "This is a test message",
    }

    res = api_client.post(
        CONTACT_URL,
        payload,
        format="json",
        REMOTE_ADDR="1.2.3.4",
        HTTP_USER_AGENT="pytest-agent",
    )

    assert res.status_code in (200, 201)
    assert ContactMessage.objects.count() == 1

    obj = ContactMessage.objects.first()
    assert obj.full_name == payload["full_name"]
    assert obj.email == payload["email"]
    assert obj.subject == payload["subject"]
    assert obj.message == payload["message"]
    assert obj.ip_address in ("1.2.3.4", None)
    assert obj.user_agent is not None


@pytest.mark.django_db
def test_contact_create_requires_full_name(api_client):
    payload = {
        "name": "Wrong field",  # fault
        "email": "test@example.com",
        "subject": "Hello",
        "message": "This is a test message",
    }

    res = api_client.post(CONTACT_URL, payload, format="json")

    assert res.status_code == 400
    # full_name required
    assert "full_name" in res.data


@pytest.mark.django_db
def test_newsletter_subscribe_creates_new(api_client):
    payload = {"email": "nl_test@example.com"}

    res = api_client.post(NEWSLETTER_SUB_URL, payload, format="json")

    assert res.status_code == 201
    assert res.data.get("detail") == "Subscribed."
    assert NewsletterSubscriber.objects.count() == 1

    obj = NewsletterSubscriber.objects.first()
    assert obj.email == "nl_test@example.com"
    assert obj.is_active is True


@pytest.mark.django_db
def test_newsletter_subscribe_idempotent(api_client):
    payload = {"email": "nl_test@example.com"}

    res1 = api_client.post(NEWSLETTER_SUB_URL, payload, format="json")
    res2 = api_client.post(NEWSLETTER_SUB_URL, payload, format="json")

    assert res1.status_code == 201
    assert res2.status_code == 200
    assert res2.data.get("detail") == "Already subscribed."
    assert NewsletterSubscriber.objects.count() == 1


@pytest.mark.django_db
def test_newsletter_subscribe_lowercases_email(api_client):
    payload = {"email": "NL_Test@Example.Com"}

    res = api_client.post(NEWSLETTER_SUB_URL, payload, format="json")

    assert res.status_code == 201
    obj = NewsletterSubscriber.objects.get()
    assert obj.email == "nl_test@example.com"


@pytest.mark.django_db
def test_newsletter_subscribe_reactivates_if_inactive(api_client):
    obj = NewsletterSubscriber.objects.create(email="inactive@example.com", is_active=False,)
    
    if hasattr(obj, "unsubscribed_date"):
        obj.unsubscribed_date = obj.created_date
        obj.save(update_fields=["unsubscribed_date"])

    res = api_client.post(NEWSLETTER_SUB_URL, {"email": "inactive@example.com"}, format="json")

    assert res.status_code == 201
    obj.refresh_from_db()
    assert obj.is_active is True
    if hasattr(obj, "unsubscribed_date"):
        assert obj.unsubscribed_date is None

