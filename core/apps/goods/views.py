from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render

from goods.models import Products


def catalog(request, category_slug, page=1):

    if category_slug == 'vse-tovary':
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))
    
    # количество товаров на страницу
    paginator = Paginator(goods, 6)
    # отображение первой страницы
    current_page = paginator.page(page)
    
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
