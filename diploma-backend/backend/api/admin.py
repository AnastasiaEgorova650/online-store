from django.contrib import admin

# # from products.models import (
# #     Category,
# #     Subcategory,
# #     Tag,
# #     Review,
# #     Product,
# #     ProductImage,
# #     Specification,
# # )
#
#
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = "pk", "title", "image"
#     list_display_links = "pk", "title"
#     ordering = ("pk", )
#     search_fields = ("title", )
#
#
# @admin.register(Subcategory)
# class SubcategoryAdmin(admin.ModelAdmin):
#     list_display = "pk", "title", "image"
#     list_display_links = "pk", "title"
#     ordering = ("pk",)
#     search_fields = ("title",)
#
#
# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = "pk", "name"
#     list_display_links = "pk", "name"
#     ordering = ("pk", )
#     search_fields = ("name", )
#
#
# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = "pk", "author", "text", "rate", "date", "product"
#     list_display_links = "pk", "author"
#     ordering = ("pk", )
#     search_fields = "author", "product"
#
#
# @admin.register(Specification)
# class Specification(admin.ModelAdmin):
#     list_display = "pk", "name", "value"
#     list_display_links = "pk", "name"
#     ordering = ("-name", )
#     search_fields = ("name", )
#
#
# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [
#         ProductImageInline,
#     ]
#
#     list_display = [
#         "pk",
#         "title",
#         "description",
#         "full_description",
#         "price",
#         "date",
#         "freeDelivery",
#         "category",
#     ]
#     list_display_links = "pk", "title"
#     ordering = ("pk", )
#     search_fields = ("title", )
#
#     def description_short(self, obj: Product):
#         if len(obj.description) < 20:
#             return obj.description
#         return obj.description[:120] + "..."
#


