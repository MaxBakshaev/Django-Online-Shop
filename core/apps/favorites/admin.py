# from django.contrib import admin

# from favorites.models import Favorite


# class FavoriteTabAdmin(admin.TabularInline):
#     model = Favorite
#     fields = "product", "created_timestamp"
#     search_fields = "product", "created_timestamp"
#     readonly_fields = ("created_timestamp",)
#     extra = 1


# @admin.register(Favorite)
# class FavoriteAdmin(admin.ModelAdmin):
#     list_display = ["user_display", "product_display", "created_timestamp",]
#     list_filter = ["created_timestamp", "user", "product__name",]

#     def user_display(self, obj):
#         if obj.user:
#             return str(obj.user)
#         return "Анонимный пользователь"

#     def product_display(self, obj):

#         return str(obj.product.name)
