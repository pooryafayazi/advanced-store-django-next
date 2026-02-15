# backend\shop\api_urls.py
from django.urls import path
from . import api_views


app_name= 'shop'


urlpatterns = [
    path("products/", api_views.ShopProductGridAPIView.as_view(), name="product-grid"),
    path("products/<slug:slug>/", api_views.ShopProductDetailAPIView.as_view(), name="product-detail"),
    path("categories/", api_views.CategoryListAPIView.as_view(), name="categories"),
    path("wishlist/toggle/", api_views.WishlistToggleAPIView.as_view(), name="wishlist-toggle"),
    path("wishlist/", api_views.WishlistListAPIView.as_view(), name="wishlist-list"),
]
