from django.contrib import admin

from carts.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display: list[str] = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]
    search_fields: list[str] = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]

    inlines = [CartTabAdmin, OrderTabulareAdmin]
