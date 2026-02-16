# backend\cart\tests\test_api.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from shop.models import ProductModel, ProductCategoryModel, ProductStatusTypeModel


pytestmark = pytest.mark.django_db

BASE = "/api/cart"


def url(suffix: str) -> str:
    # expected endpoints:
    # /api/cart/add/
    # /api/cart/update/
    # /api/cart/remove/
    # /api/cart/summary/
    return f"{BASE}/{suffix}/"


@pytest.fixture
def client():
    # acts like a browser and maintains cookies/sessions 
    return APIClient()


@pytest.fixture
def seller():
    U = get_user_model()
    return U.objects.create_user(email="seller@example.com", password="Pass@12345")


@pytest.fixture
def category():
    return ProductCategoryModel.objects.create(title="Cat", slug="cat")


@pytest.fixture
def product(seller, category):
    p = ProductModel.objects.create(
        created_by=seller,
        title="Test Product",
        slug="test-product-cart",
        description="desc",
        brief_description="brief",
        stock=10,
        status=ProductStatusTypeModel.publish.value,
        price=100000,
        discount_percent=0,
    )
    p.categories.add(category)
    return p


def assert_empty(summary: dict):
    assert summary["items"] == []
    assert summary["total_qty"] == 0
    assert summary["total_price"] == 0


def test_cart_summary_empty(client):
    res = client.get(url("summary"))
    assert res.status_code == 200
    assert_empty(res.json())


def test_cart_add_and_persist_in_session(client, product):
    res = client.post(url("add"), {"product_id": product.id, "quantity": 2}, format="json")
    assert res.status_code == 200

    data = res.json()
    assert data["total_qty"] == 2
    assert len(data["items"]) == 1

    item = data["items"][0]
    assert item["product_id"] == product.id
    assert item["qty"] == 2
    assert item["final_price"] == int(product.get_final_price())
    assert item["line_total"] == int(product.get_final_price()) * 2

    # same client => same session => the cart has to be remaind
    res2 = client.get(url("summary"))
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["total_qty"] == 2
    assert len(data2["items"]) == 1


def test_cart_add_accumulates_quantity(client, product):
    client.post(url("add"), {"product_id": product.id, "quantity": 2}, format="json")
    res = client.post(url("add"), {"product_id": product.id, "quantity": 3}, format="json")

    assert res.status_code == 200
    data = res.json()
    assert data["total_qty"] == 5
    assert data["items"][0]["qty"] == 5


def test_cart_update_sets_quantity(client, product):
    client.post(url("add"), {"product_id": product.id, "quantity": 5}, format="json")
    res = client.post(url("update"), {"product_id": product.id, "quantity": 2}, format="json")

    assert res.status_code == 200
    data = res.json()
    assert data["total_qty"] == 2
    assert data["items"][0]["qty"] == 2


def test_cart_update_zero_removes_item(client, product):
    client.post(url("add"), {"product_id": product.id, "quantity": 1}, format="json")
    res = client.post(url("update"), {"product_id": product.id, "quantity": 0}, format="json")

    assert res.status_code == 200
    assert_empty(res.json())


def test_cart_remove_endpoint(client, product):
    client.post(url("add"), {"product_id": product.id, "quantity": 1}, format="json")
    res = client.post(url("remove"), {"product_id": product.id}, format="json")

    assert res.status_code == 200
    assert_empty(res.json())


def test_cart_add_unknown_product_returns_404(client):
    res = client.post(url("add"), {"product_id": 999999, "quantity": 1}, format="json")
    assert res.status_code == 404


def test_cart_summary_skips_unpublished_products(client, product):
    client.post(url("add"), {"product_id": product.id, "quantity": 2}, format="json")

    # the  product out off publish
    product.status = ProductStatusTypeModel.draft.value
    product.save(update_fields=["status"])

    res = client.get(url("summary"))
    assert res.status_code == 200
    assert_empty(res.json())
