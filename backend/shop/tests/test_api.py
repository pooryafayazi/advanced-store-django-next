# backend/shop/tests/test_api.py
import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from shop.models import (
    ProductCategoryModel,
    ProductModel,
    ProductImageModel,
    WishlistProductModel,
    ProductStatusTypeModel,
)

pytestmark = pytest.mark.django_db

API_PRODUCTS = "/api/shop/products/"
API_CATEGORIES = "/api/shop/categories/"
API_WISHLIST_TOGGLE = "/api/shop/wishlist/toggle/"
API_WISHLIST_LIST = "/api/shop/wishlist/"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    U = get_user_model()
    return U.objects.create_user(email="u1@example.com", password="Pass@12345")


@pytest.fixture
def seller():
    U = get_user_model()
    return U.objects.create_user(email="seller@example.com", password="Pass@12345", is_staff=True)


@pytest.fixture
def cat_electronics():
    return ProductCategoryModel.objects.create(title="Electronics", slug="electronics")


@pytest.fixture
def cat_phones(cat_electronics):
    return ProductCategoryModel.objects.create(title="Phones", slug="phones", parent=cat_electronics)


@pytest.fixture
def published_product(seller, cat_phones):
    p = ProductModel.objects.create(
        created_by=seller,
        title="iPhone 13",
        slug="iphone-13",
        description="desc",
        brief_description="brief",
        stock=5,
        status=ProductStatusTypeModel.publish.value,
        price=Decimal("1000"),
        discount_percent=10,
    )
    p.categories.add(cat_phones)
    ProductImageModel.objects.create(
        product=p,
        file="product/extra-img/x.png",
        is_cover=True,
        sort_order=0,
    )
    return p


@pytest.fixture
def draft_product(seller, cat_phones):
    p = ProductModel.objects.create(
        created_by=seller,
        title="Draft Item",
        slug="draft-item",
        description="desc",
        stock=5,
        status=ProductStatusTypeModel.draft.value,
        price=Decimal("2000"),
        discount_percent=0,
    )
    p.categories.add(cat_phones)
    return p


def test_categories_list(api_client, cat_electronics, cat_phones):
    res = api_client.get(API_CATEGORIES)
    assert res.status_code == 200
    slugs = [x["slug"] for x in res.json()]
    assert "electronics" in slugs
    assert "phones" in slugs


def test_product_grid_returns_only_published(api_client, published_product, draft_product):
    res = api_client.get(API_PRODUCTS)
    assert res.status_code == 200
    slugs = [x["slug"] for x in res.json()]
    assert published_product.slug in slugs
    assert draft_product.slug not in slugs


def test_product_grid_search_q(api_client, published_product):
    res = api_client.get(API_PRODUCTS, {"q": "iphone"})
    assert res.status_code == 200
    assert any(x["slug"] == published_product.slug for x in res.json())


def test_product_grid_filter_category(api_client, published_product):
    res = api_client.get(API_PRODUCTS, {"category": "phones"})
    assert res.status_code == 200
    assert any(x["slug"] == published_product.slug for x in res.json())


def test_product_detail(api_client, published_product):
    res = api_client.get(f"{API_PRODUCTS}{published_product.slug}/")
    assert res.status_code == 200
    data = res.json()
    assert data["slug"] == published_product.slug
    assert "images" in data
    assert "categories" in data
    # بسته به DRF ممکنه عدد رو string بده
    assert str(data["final_price"]) in ("900", "900.0")


def test_product_detail_404_for_draft(api_client, draft_product):
    res = api_client.get(f"{API_PRODUCTS}{draft_product.slug}/")
    assert res.status_code == 404


def test_wishlist_requires_auth(api_client, published_product):
    res = api_client.post(API_WISHLIST_TOGGLE, {"product_id": published_product.id}, format="json")
    assert res.status_code in (401, 403)


def test_wishlist_toggle_add_and_remove(api_client, user, published_product):
    api_client.force_authenticate(user=user)

    res = api_client.post(API_WISHLIST_TOGGLE, {"product_id": published_product.id}, format="json")
    assert res.status_code == 201
    assert res.json()["in_wishlist"] is True
    assert WishlistProductModel.objects.filter(user=user, product=published_product).exists()

    res = api_client.get(API_WISHLIST_LIST)
    assert res.status_code == 200
    assert any(x["slug"] == published_product.slug for x in res.json())

    res = api_client.post(API_WISHLIST_TOGGLE, {"product_id": published_product.id}, format="json")
    assert res.status_code == 200
    assert res.json()["in_wishlist"] is False
    assert not WishlistProductModel.objects.filter(user=user, product=published_product).exists()


def test_in_wishlist_flag_on_grid(api_client, user, published_product):
    api_client.force_authenticate(user=user)
    WishlistProductModel.objects.create(user=user, product=published_product)

    res = api_client.get(API_PRODUCTS)
    assert res.status_code == 200
    data = res.json()
    target = next(x for x in data if x["slug"] == published_product.slug)
    assert target["in_wishlist"] is True
