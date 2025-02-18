from typing import Any
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.db.models.base import Model as Model
from django.shortcuts import render
from django.views.generic import DetailView

from goods.utils import q_search
from goods.models import Categories, Products


def catalog(request, category_slug=None):

    # параметры для пагинации и фильтров
    page = request.GET.get("page", 1)
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", None)
    query = request.GET.get("q", None)
    cost_1k = request.GET.get("cost_1k", None)
    cost_10k = request.GET.get("cost_10k", None)
    cost_100k = request.GET.get("cost_100k", None)
    cost_1m = request.GET.get("cost_1m", None)
    cost_10m = request.GET.get("cost_10m", None)

    # создается базовый запрос к БД (QuerySet)
    if category_slug == "vse-tovary":
        goods = Products.objects.all()

    elif query:
        goods = q_search(query)

    else:
        goods = Products.objects.filter(category__slug=category_slug)

    # Проверки с добавлением фильтров к запросу
    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)


    # Eсли выбран 1 параметр цены
    if cost_1k and not cost_10k and not cost_100k and not cost_1m and not cost_10m:
        goods = goods.filter(price__lt=1_000)

    if cost_10k and not cost_1k and not cost_100k and not cost_1m and not cost_10m:
        goods = goods.filter(price__lt=10_000, price__gt=1_000)

    if cost_100k and not cost_1k and not cost_10k and not cost_1m and not cost_10m:
        goods = goods.filter(price__lt=100_000, price__gt=10_000)

    if cost_1m and not cost_1k and not cost_10k and not cost_100k and not cost_10m:
        goods = goods.filter(price__lt=1_000_000, price__gt=100_000)

    if cost_10m and not cost_1k and not cost_10k and not cost_100k and not cost_1m:
        goods = goods.filter(price__gt=1_000_000)


    # Eсли выбрано 2 параметра цены
    if cost_1k and cost_10k and not cost_100k and not cost_1m and not cost_10m:
        goods = goods.filter(price__lt=10_000)

    if cost_10k and cost_100k and not cost_1k and not cost_1m and not cost_10m:
        goods = goods.filter(price__lt=100_000, price__gt=10_000)

    if cost_100k and cost_1m and not cost_1k and not cost_10k and not cost_10m:
        goods = goods.filter(price__lt=1_000_000, price__gt=100_000)

    if cost_1m and cost_10m and not cost_1k and not cost_10k and not cost_100k:
        goods = goods.filter(price__gt=1_000_000)


    # Eсли выбрано 3 параметра цены
    if cost_1k and cost_10k and cost_100k and not cost_1m and not cost_10m:
        goods = goods.filter(price__lt=100_000)

    if cost_10k and cost_100k and cost_1m and not cost_1k and not cost_10m:
        goods = goods.filter(price__lt=1_000_000, price__gt=10_000)

    if cost_100k and cost_1m and cost_10m and not cost_1k and not cost_10k:
        goods = goods.filter(price__gt=100_000)


    # Eсли выбрано 4 параметра цены
    if cost_1k and cost_10k and cost_100k and cost_1m and not cost_10m:
        goods = goods.filter(price__lt=1_000_000)

    if cost_10k and cost_100k and cost_1m and cost_10m and not cost_1k:
        goods = goods.filter(price__gt=1_000)


    amount = len(goods)

    paginator = Paginator(goods, 6)

    # отображение текущей страницы
    current_page = paginator.page(int(page))

    if not query:
        
        category = Categories.objects.get(slug=category_slug)
        
        context = {
            "title": f"MultiShop - Каталог - {category.name}",
            "check_page": "MultiShop - Категории",
            "goods": current_page,
            "slug_url": category_slug,
            "amount": amount,
            "category": category,
        }
    
    else:

        context = {
            "title": "MultiShop - Каталог - Поиск",
            "check_page": "MultiShop - Категории",
            "goods": current_page,
            "amount": amount,
        }

    return render(request, "goods/catalog.html", context)


class ProductView(DetailView):
    
    template_name = "goods/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"
    
    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        context["check_page"] = "MultiShop - Продукты"
        return context
