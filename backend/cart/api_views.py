# backend\cart\api_views.py
from decimal import Decimal

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import ProductModel, ProductStatusTypeModel
from .serializers import CartAddSerializer, CartUpdateSerializer, CartRemoveSerializer


CART_SESSION_KEY = "cart"  # session["cart"] = {"<product_id>": {"qty": 2}, ...}


def _get_cart(session):
    return session.get(CART_SESSION_KEY, {})


def _save_cart(session, cart):
    session[CART_SESSION_KEY] = cart
    session.modified = True


def _build_summary(cart):
    """
    Output for Next.js:
    items: list and product info
    total_qty:
    total_price: 
    """
    ids = [int(pid) for pid in cart.keys()]
    if not ids:
        return {"items": [], "total_qty": 0, "total_price": 0}
    
    products = (ProductModel.objects.filter(id__in=ids, status=ProductStatusTypeModel.publish.value).prefetch_related("categories"))
    by_id = {p.id: p for p in products}

    items = []
    total_qty = 0
    total_price = 0

    # for remove/unpublish, have not to be in summary
    for pid_str, data in cart.items():
        pid = int(pid_str)
        p = by_id.get(pid)
        if not p:
            continue

        qty = int(data.get("qty", 0))
        if qty <= 0:
            continue

        unit_price = int(p.price)
        final_price = int(p.get_final_price())
        line_total = final_price * qty

        items.append({
            "product_id": p.id,
            "title": p.title,
            "slug": p.slug,
            "image": str(p.image) if p.image else "",
            "qty": qty,
            "unit_price": unit_price,
            "final_price": final_price,
            "discount_percent": int(p.discount_percent),
            "line_total": line_total,
        })

        total_qty += qty
        total_price += line_total
    
    return {"items": items, "total_qty": total_qty, "total_price": total_price}


class CartAddAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []   # denaied for CSRF authentication in POST

    def post(self, request):
        ser = CartAddSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        product_id = ser.validated_data["product_id"]
        qty = ser.validated_data["quantity"]

        product = get_object_or_404(ProductModel, id=product_id, status=ProductStatusTypeModel.publish.value)

        cart = _get_cart(request.session)
        pid = str(product.id)
        cart.setdefault(pid, {"qty": 0})
        cart[pid]["qty"] = int(cart[pid]["qty"]) + int(qty)

        _save_cart(request.session, cart)
        return Response(_build_summary(cart), status=status.HTTP_200_OK)


class CartUpdateAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        ser = CartUpdateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        product_id = ser.validated_data["product_id"]
        qty = ser.validated_data["quantity"]

        cart = _get_cart(request.session)
        pid = str(product_id)

        if qty <= 0:
            cart.pop(pid, None)
        else:
            cart[pid] = {"qty": int(qty)}
        
        _save_cart(request.session, cart)
        return Response(_build_summary(cart), status=status.HTTP_200_OK)


class CartRemoveAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        ser = CartRemoveSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        product_id = ser.validated_data["product_id"]
        cart = _get_cart(request.session)
        cart.pop(str(product_id), None)

        _save_cart(request.session, cart)
        return Response(_build_summary(cart), status=status.HTTP_200_OK)


class CartSummaryAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        cart = _get_cart(request.session)
        return Response(_build_summary(cart), status=status.HTTP_200_OK)

