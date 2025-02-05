from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render

from goods.utils import q_search
from goods.models import Products


def catalog(request, category_slug=None):

    # параметры для пагинации и фильтров
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)
    cost_1000 = request.GET.get('cost_1000', None)
    cost_10000 = request.GET.get('cost_10000', None)
    cost_100000 = request.GET.get('cost_100000', None)
    cost_1000000 = request.GET.get('cost_1000000', None)
    cost_10000000 = request.GET.get('cost_10000000', None)
    
    # создается базовый запрос к БД (QuerySet)
    if category_slug == 'vse-tovary':
        goods = Products.objects.all()
        
        # проверки с добавлением фильтров к запросу
        if on_sale:
            goods = goods.filter(discount__gt=0)
        
        if order_by and order_by != "default":
            goods = goods.order_by(order_by)
            
        if cost_1000:
            goods = goods.filter(price__lt=1000)
        
        if cost_10000:
            goods = goods.filter(price__lt=10000, price__gt=1000)
            
        if cost_100000:
            goods = goods.filter(price__lt=100000, price__gt=10000)
        
        if cost_1000000:
            goods = goods.filter(price__lt=1000000, price__gt=100000)
        
        if cost_10000000:
            goods = goods.filter(price__gt=1000000)
            
    elif query:
        goods = q_search(query)
        
    else:
        category_filter = Products.objects.filter(category__slug=category_slug)
        goods = get_list_or_404(category_filter)
        
        # проверки с добавлением фильтров к запросу
        if on_sale:
            category_filter = category_filter.filter(discount__gt=0)
        
        if order_by and order_by != "default":
            category_filter = category_filter.order_by(order_by)
            
        if cost_1000:
            category_filter = category_filter.filter(price__lt=1000)
        
        if cost_10000:
            category_filter = category_filter.filter(price__lt=10000, price__gt=1000)
            
        if cost_100000:
            category_filter = category_filter.filter(price__lt=100000, price__gt=10000)
        
        if cost_1000000:
            category_filter = category_filter.filter(price__lt=1000000, price__gt=100000)
        
        if cost_10000000:
            category_filter = category_filter.filter(price__gt=1000000)
            
        goods = get_list_or_404(category_filter)
    
        
    amount = len(goods)
    
    # количество товаров на страницу
    
    # show_three = request.GET.get('show_three', 3)
    # show_six = request.GET.get('show_six', 6)
    # show_nine = request.GET.get('show_nine', 9)
    # show_twelve = request.GET.get('show_twelve', 12)
    
    paginator = Paginator(goods, 6)
    
    # if show_three:
    #     paginator = Paginator(goods, show_three)
    # elif show_nine:
    #     paginator = Paginator(goods, show_nine)
    # elif show_twelve:
    #     paginator = Paginator(goods, show_twelve)
    # else:
    #     paginator = Paginator(goods, show_six)
        
    # отображение первой страницы
    current_page = paginator.page(int(page))
    
    context = {
        "title": "MultiShop - Каталог",
        "goods": current_page,
        "slug_url": category_slug,
        "amount": amount
    }

    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    
    # метод get для получения одной записи
    product = Products.objects.get(slug=product_slug)
    
    context = {
        "product": product
    }
    
    return render(request, "goods/product.html", context=context)
