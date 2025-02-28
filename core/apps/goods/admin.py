from django.contrib import admin

from goods.models import Categories, Products, Review


# Регистрация моделей в админ панели

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):  
    
    # отображение в http://127.0.0.1:8000/admin/goods/categories/ :

    # автоматически набирается текст для ссылки после ввода названия
    prepopulated_fields = {"slug": ("name",)}  
    # отображение полей на странице списка категорий
    list_display = ["name",]
    

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):  
    
    # отображение в http://127.0.0.1:8000/admin/goods/products/ :
     
    # автоматически набирается текст для ссылки после ввода названия
    prepopulated_fields = {"slug": ("name",)}
    # отображение полей на странице списка продуктов
    list_display = ["name", "quantity", "price", "discount"]
    # редактируемые параметры
    list_editable = ["discount",]  
    # поиск по параметрам
    search_fields = ["name", "description"]
    # фильтр по скидке, количеству, категории
    list_filter = ["discount", "quantity", "category"]
    
    # Отображение на странице добавления или изменения параметров товара :
    
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


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created')
    list_filter = ('user', 'created')
    search_fields = ('product', 'user', 'comment')
admin.site.register(Review, ReviewAdmin)