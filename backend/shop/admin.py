# backend\shop\admin.py
from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .models import ProductCategoryModel, ProductModel, ProductImageModel, WishlistProductModel


@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "parent", "created_date", "updated_date")
    list_filter = ("parent", "created_date", "updated_date")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_date",)


class ProductImageInline(admin.TabularInline):
    model = ProductImageModel
    extra = 1
    fields = ("file", "is_cover", "sort_order", "created_date", "updated_date")
    readonly_fields = ("created_date", "updated_date")
    ordering = ("sort_order", "-created_date")


@admin.action(description="Mark selected products as PUBLISHED")
def make_published(modeladmin, request, queryset):
    queryset.update(status=1)


@admin.action(description="Mark selected products as DRAFT")
def make_draft(modeladmin, request, queryset):
    queryset.update(status=2)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

    list_display = (
        "id",
        "title",
        "slug",
        "status",
        "stock",
        "price",
        "discount_percent",
        "final_price",
        "created_by",
        "created_date",
        "updated_date",
    )
    list_filter = (
        "status",
        "created_date",
        "updated_date",
        "categories",
    )
    search_fields = ("title", "slug", "description", "brief_description")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("created_by",)
    filter_horizontal = ("categories",)
    ordering = ("-created_date",)
    actions = [make_published, make_draft]

    readonly_fields = ("created_date", "updated_date", "avg_rate", "rate_count")

    fieldsets = (
        (_("Basic"), {"fields": ("title", "slug", "status", "created_by")}),
        (_("Categories"), {"fields": ("categories",)}),
        (_("Content"), {"fields": ("image", "brief_description", "description")}),
        (_("Pricing & Stock"), {"fields": ("price", "discount_percent", "stock")}),
        (_("Rating"), {"fields": ("avg_rate", "rate_count")}),
        (_("Timestamps"), {"fields": ("created_date", "updated_date")}),
    )

    @admin.display(description="Final Price")
    def final_price(self, obj: ProductModel):
        try:
            return obj.get_final_price()
        except Exception:
            return "-"

    def save_formset(self, request, form, formset, change):
        """
        Ensure only ONE cover image per product (admin-side guard).
        (DB constraint also exists, but this gives a nicer admin behavior.)
        """
        instances = formset.save(commit=False)
        for inst in instances:
            inst.save()
        formset.save_m2m()

        product = form.instance
        if ProductImageModel.objects.filter(product=product, is_cover=True).count() > 1:
            # keep the newest as cover, unset others
            covers = ProductImageModel.objects.filter(product=product, is_cover=True).order_by("-created_date")
            keep = covers.first()
            covers.exclude(pk=keep.pk).update(is_cover=False)


@admin.register(ProductImageModel)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "is_cover", "sort_order", "created_date", "updated_date")
    list_filter = ("is_cover", "created_date", "updated_date")
    search_fields = ("product__title", "product__slug")
    ordering = ("-created_date",)


@admin.register(WishlistProductModel)
class WishlistProductAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "created_date", "updated_date")
    list_filter = ("created_date", "updated_date")
    search_fields = ("user__email", "product__title", "product__slug")
    autocomplete_fields = ("user", "product")
    ordering = ("-created_date",)
