from django.contrib import admin

from .models import Draw, Ticket, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("vk_id", "full_name", "created_at")
    search_fields = ("vk_id", "full_name")
    ordering = ("-created_at",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("number", "user", "issued_at")
    search_fields = ("number", "user__full_name", "user__vk_id")
    ordering = ("number",)


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ("title", "total_winners", "created_at")
    filter_horizontal = ("winners",)
