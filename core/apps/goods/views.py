from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render

from goods.models import Products


def catalog(request, category_slug):

    # параметры для пагинации и фильтров
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    
    # создается базовый запрос к БД (QuerySet)
    if category_slug == 'vse-tovary':
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    # проверки с добавлением фильтров к запросу
    if on_sale:
        goods = goods.filter(discount__gt=0)
    if order_by and order_by != "default":
        goods = goods.order_by(order_by)
    
    # количество товаров на страницу
    paginator = Paginator(goods, 6)
    # отображение первой страницы
    current_page = paginator.page(int(page))
    
    context = {
        "title": "MultiShop - Каталог",
        "goods": current_page,
        "slug_url": category_slug
    }

    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    
    # метод get для получения одной записи
    product = Products.objects.get(slug=product_slug)
    
    context = {
        "product": product
    }
    
    return render(request, "goods/product.html", context=context)
