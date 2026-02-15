# backend\shop\models.py
from decimal import Decimal

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductStatusTypeModel(models.IntegerChoices):
    publish = 1, _("publish")
    draft = 2, _("draft")


class ProductCategoryModel(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, unique=True, db_index=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children",)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.title


class ProductModel(TimeStampedModel):
    created_by = models.ForeignKey("accounts.User", on_delete=models.PROTECT, related_name="products",)
    categories = models.ManyToManyField(ProductCategoryModel, related_name="products", blank=True)

    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, unique=True, db_index=True)

    image = models.ImageField(upload_to="product/img/", default="default/product-image.png",  blank=True,)

    description = models.TextField()
    brief_description = models.TextField(null=True, blank=True)

    stock = models.PositiveIntegerField(default=0, db_index=True)
    status = models.IntegerField(choices=ProductStatusTypeModel.choices, default=ProductStatusTypeModel.draft.value, db_index=True,)

    price = models.DecimalField(default=0, max_digits=12, decimal_places=0, db_index=True)
    discount_percent = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],)

    avg_rate = models.DecimalField(default=Decimal("0.00"), max_digits=4, decimal_places=2)
    rate_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_date"]
        indexes = [models.Index(fields=["status", "-created_date"]), models.Index(fields=["price"]),]

    def __str__(self):
        return self.title

    @property
    def is_discounted(self) -> bool:
        return self.discount_percent > 0

    @property
    def is_published(self) -> bool:
        return self.status == ProductStatusTypeModel.publish.value

    def get_final_price(self) -> Decimal:
        discount_rate = (Decimal(self.discount_percent) / Decimal("100"))
        discount_amount = (self.price * discount_rate)
        final_price = self.price - discount_amount
        return final_price.quantize(Decimal("1"))


class ProductImageModel(TimeStampedModel):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="images")
    file = models.ImageField(upload_to="product/extra-img/")
    is_cover = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-created_date"]
        constraints = [models.UniqueConstraint(fields=["product"], condition=models.Q(is_cover=True), name="unique_cover_image_per_product",)]


class WishlistProductModel(TimeStampedModel):
    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT, related_name="wishlist_items")
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="wishlisted_by")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "product"], name="unique_user_product_wishlist")]

    def __str__(self):
        return f"{self.user.email} -> {self.product.title}"


