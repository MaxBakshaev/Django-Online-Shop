from django.shortcuts import render

from goods.models import Products


def catalog(request, category_slug):

    if category_slug == 'vse-tovary':
        goods = Products.objects.all()
    else:
        goods = Products.objects.filter(category__slug=category_slug)
    

    context = {
        "title": "MultiShop - Каталог",
        "goods": goods,
    }

    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    
    # метод get для получения одной записи
    product = Products.objects.get(slug=product_slug)
    
    context = {
        "product": product
    }
    
    return render(request, "goods/product.html", context=context)
