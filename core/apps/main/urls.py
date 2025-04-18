from django.urls import path

from main import views


app_name = 'main'

# Аргументы Path:
# '' , 'about' и т.д. - URL-маршрут сайта
# второй аргумент - функция из контроллера views
# name - имя в шаблоне для URL-адреса
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('all_categories/', views.All_categories.as_view(), name='all_categories'),
]
