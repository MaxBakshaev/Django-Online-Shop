from django.contrib import admin

from goods.models import Categories, Products


# Регистрация моделей в админ панели
admin.site.register(Categories)
admin.site.register(Products)