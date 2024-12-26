from django.shortcuts import render
from django.http import HttpResponse

from goods.models import Categories


def index(request):
    
    # список из всех категорий
    categories = Categories.objects.all()
    
    # контекстные переменные, передаются в шаблон
    context = {
        'title': 'MultiShop - Главная',
        'categories': categories
    }
    
    # функция render отрисовывает страницу
    return render(request, 'main/index.html', context)


def about(request):
    
    context = {
        'title': 'MultiShop - О нас',
        'content': 'MultiShop - Товары на все случаи жизни',
        'text_on_page': 'Лучший магазин во вселенной'
    }
    
    return render(request, 'main/about.html', context)
