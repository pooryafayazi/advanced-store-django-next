# backend\cart\api_urls.py
from django.urls import path
from . import api_views


app_name= 'cart'


urlpatterns = [
    path("add/", api_views.CartAddAPIView.as_view(), name="cart-add"),
    path("update/", api_views.CartUpdateAPIView.as_view(), name="cart-update"),
    path("remove/", api_views.CartRemoveAPIView.as_view(), name="cart-remove"),
    path("summary/", api_views.CartSummaryAPIView.as_view(), name="cart-summary"),
]
