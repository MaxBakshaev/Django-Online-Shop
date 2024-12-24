from django.urls import path

from main import views


app_name = 'main'

# Аргументы Path:
# '' , 'about' и т.д. - URL-маршрут сайта
# второй аргумент - функция из контроллера views
# name - имя в шаблоне для URL-адреса
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]
