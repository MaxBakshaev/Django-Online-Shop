from django.shortcuts import render
from django.http import HttpResponse

from goods.models import Products


def index(request):  
    
    discount_goods = ((Products.objects.all()).filter(discount__gt=0)).order_by('-discount')[:8]
    discount_product_1 = discount_goods[0]
    discount_product_2 = discount_goods[1]
    discount_product_3 = discount_goods[2]
    discount_product_4 = discount_goods[3]
    discount_product_5 = discount_goods[4]
    discount_product_6 = discount_goods[5]
    discount_product_7 = discount_goods[6]
    discount_product_8 = discount_goods[7]
    
    id_goods = Products.objects.all().order_by('-id')
    new_product_1 = id_goods[0]
    new_product_2 = id_goods[1]
    new_product_3 = id_goods[2]
    new_product_4 = id_goods[3]
    new_product_5 = id_goods[4]
    new_product_6 = id_goods[5]
    new_product_7 = id_goods[6]
    new_product_8 = id_goods[7]
    
    # контекстные переменные, передаются в шаблон
    context = {
        'title': 'MultiShop - Главная',  
        
        'product_1': discount_product_1,
        'product_2': discount_product_2,
        'product_3': discount_product_3,
        'product_4': discount_product_4,
        'product_5': discount_product_5,
        'product_6': discount_product_6,
        'product_7': discount_product_7,
        'product_8': discount_product_8,
        
        'new_product_1': new_product_1,
        'new_product_2': new_product_2,
        'new_product_3': new_product_3,
        'new_product_4': new_product_4,
        'new_product_5': new_product_5,
        'new_product_6': new_product_6,
        'new_product_7': new_product_7,
        'new_product_8': new_product_8
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
