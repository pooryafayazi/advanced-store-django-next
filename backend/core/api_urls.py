# backend\core\api_urls.py
from django.urls import path, re_path, include
from . import api_views


urlpatterns = [
    # path("health/", api_views.health, name="api-health"),
    re_path(r"^health/?$", api_views.health, name="api-health"),
    path("accounts/", include("accounts.api_urls")),
    path("communications/", include("communications.api_urls")),
    path("shop/", include("shop.api_urls")),

]

