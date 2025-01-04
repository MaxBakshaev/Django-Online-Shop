from django.shortcuts import render
from django.http import HttpResponse

from goods.models import Products


def index(request):
    
    order_by = request.GET.get('order_by', None)
    
    goods = ((Products.objects.all()).filter(discount__gt=0)).order_by('-discount')[:8]
    product_1 = goods[0]
    product_2 = goods[1]
    product_3 = goods[2]
    product_4 = goods[3]
    product_5 = goods[4]
    product_6 = goods[5]
    product_7 = goods[6]
    product_8 = goods[7]
    
    # контекстные переменные, передаются в шаблон
    context = {
        'title': 'MultiShop - Главная',
        'product_1': product_1,
        'product_2': product_2,
        'product_3': product_3,
        'product_4': product_4,
        'product_5': product_5,
        'product_6': product_6,
        'product_7': product_7,
        'product_8': product_8
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
