from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
            "pk", "user", "name", "surname", "phone", "email", "avatar"
            )

    list_display_links = "pk", "user"
    ordering = ("pk", )
    search_fields = ("name", "surname", "phone", "email")