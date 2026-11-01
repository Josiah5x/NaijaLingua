from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, LearnerProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("NaijaLingua Information", {
            "fields": ("role",),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("NaijaLingua Information", {
            "fields": ("role",),
        }),
    )


@admin.register(LearnerProfile)
class LearnerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "preferred_language",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    list_filter = ("preferred_language",)