from django.contrib import admin

from goods.models import Categories, Products


# Регистрация моделей в админ панели

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    # автоматически набирается текст для ссылки после ввода названия
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name",]
    
    
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "quantity", "price", "discount"]
    list_editable = ["discount",]
    search_fields = ["name", "description"]
    list_filter = ["discount", "quantity", "category"]
    # в документации много разных полей в разделе admin settings
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        ("price", "discount"),
        "quantity",
    ]
