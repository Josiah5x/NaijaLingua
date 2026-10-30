from django.contrib import admin
from .models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "native_name",
        "is_active",
        "display_order",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "native_name")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("display_order", "name")