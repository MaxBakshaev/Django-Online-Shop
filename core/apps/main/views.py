from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    
    # контекстные переменные, передаются в шаблон
    context = {
        'title': 'MultiShop - Главная'
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


def all_categories(request):
    
    context = {
        'title': 'MultiShop - Каталог',
    }
    
    return render(request, 'main/all_categories.html', context)
