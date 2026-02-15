# backend\shop\api_views.py
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ProductModel, ProductCategoryModel, WishlistProductModel, ProductStatusTypeModel
from .serializers import ProductListSerializer, ProductDetailSerializer, ProductCategorySerializer, WishlistToggleSerializer


class ShopProductGridAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        qs = (ProductModel.objects.filter(status=ProductStatusTypeModel.publish.value).prefetch_related("categories").order_by("-created_date"))

        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(title__icontains=q)

        category_slug = self.request.query_params.get("category")
        if category_slug:
            qs = qs.filter(categories__slug=category_slug)

        return qs.distinct()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx


class ShopProductDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (ProductModel.objects.filter(status=ProductStatusTypeModel.publish.value).prefetch_related("categories", "images"))

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx


class CategoryListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductCategorySerializer
    queryset = ProductCategoryModel.objects.all().order_by("-created_date")


class WishlistToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = WishlistToggleSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        product_id = ser.validated_data["product_id"]
        product = ProductModel.objects.filter(id=product_id, status=ProductStatusTypeModel.publish.value).first()

        if not product:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        obj = WishlistProductModel.objects.filter(user=request.user, product=product).first()
        if obj:
            obj.delete()
            return Response({"detail": "Removed from wishlist.", "in_wishlist": False}, status=status.HTTP_200_OK)

        WishlistProductModel.objects.create(user=request.user, product=product)
        return Response({"detail": "Added to wishlist.", "in_wishlist": True}, status=status.HTTP_201_CREATED)


class WishlistListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        product_ids = WishlistProductModel.objects.filter(user=self.request.user).values_list("product_id", flat=True)
        return (ProductModel.objects.filter(id__in=product_ids, status=ProductStatusTypeModel.publish.value).prefetch_related("categories").order_by("-created_date"))

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

