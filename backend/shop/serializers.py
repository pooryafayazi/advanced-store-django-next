# backend\shop\serializers.py
from rest_framework import serializers
from .models import ProductCategoryModel, ProductModel, ProductImageModel, WishlistProductModel


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryModel
        fields = ("id", "title", "slug", "parent")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = ("id", "file", "is_cover", "sort_order")


class ProductListSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(many=True, read_only=True)
    final_price = serializers.SerializerMethodField()
    in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = (
            "id", "title", "slug", "image",
            "brief_description", "stock",
            "price", "discount_percent", "final_price",
            "avg_rate", "rate_count",
            "categories", "in_wishlist",
            "created_date", "updated_date",)
    
    def get_final_price(self, obj):
        return obj.get_final_price()

    def get_in_wishlist(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return WishlistProductModel.objects.filter(user=request.user, product=obj).exists()



class ProductDetailSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    final_price = serializers.SerializerMethodField()
    in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = (
            "id", "title", "slug",
            "image", "images",
            "description", "brief_description",
            "stock", "status",
            "price", "discount_percent", "final_price",
            "avg_rate", "rate_count",
            "categories", "in_wishlist",
            "created_date", "updated_date",
        )

    def get_final_price(self, obj):
        return obj.get_final_price()

    def get_in_wishlist(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return WishlistProductModel.objects.filter(user=request.user, product=obj).exists()



class WishlistToggleSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


 