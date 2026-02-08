import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def test_register_creates_user_and_profile():
    c = APIClient()
    res = c.post("/api/accounts/register/", {
        "email": "u1@example.com",
        "password1": "StrongPass@12345",
        "password2": "StrongPass@12345",
        "first_name": "Poorya",
        "last_name": "Fayazi",
        "phone_number": "+989121234567",
    }, format="json")
    assert res.status_code == 201

    u = User.objects.get(email="u1@example.com")
    assert u.profile is not None
    assert u.profile.first_name == "Poorya"


@pytest.mark.django_db
def test_me_requires_auth():
    c = APIClient()
    res = c.get("/api/accounts/me/")
    assert res.status_code in (401, 403)
