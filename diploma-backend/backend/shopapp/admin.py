from django.contrib import admin

from .models import (
    Category,
    Subcategory,
    Product,
    Tag,
    Specification,
    ProductImage,
    Sale,
    Basket,
    BasketItem,
    DeliveryPrices,
    Order,
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "image"
    list_display_links = "pk", "title"
    search_fields = "title",

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "image"
    list_display_links = "pk", "title"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "price", "count"
    list_display_links = "pk", "title"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"

@admin.register(Specification)
class Specification(admin.ModelAdmin):
    list_display = "pk", "name", "value"
    list_display_links = "pk", "name", "value"

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "image"
    list_display_links = "pk", "product", "image"

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "date_from", "date_to", "discount"
    list_display_links = "pk", "product",

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = "pk", "user", "created_at"
    list_display_links = "pk", "user",

@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = "pk", "basket", "product", "quantity"
    list_display_links = "pk", "basket", "product"

@admin.register(DeliveryPrices)
class DeliveryPricesAdmin(admin.ModelAdmin):
    list_display = "pk", "delivery_cost", "delivery_express_cost", "delivery_free_minimum_cost"
    list_display_links = "pk", "delivery_cost", "delivery_express_cost", "delivery_free_minimum_cost"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "pk", "full_name", "created_at", "city", "status", "archived"
    list_display_links = "pk", "full_name", "created_at", "city"
