from typing import Any
from django.db.models import QuerySet
from django.views.generic import DetailView, ListView

from goods.utils import q_search
from goods.models import Categories, Products


class CatalogView(ListView):
    
    model = Products
    # queryset = Products.objects.all()
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 6

    def get_queryset(self) -> QuerySet[Any]:
        
        self.category_slug = self.kwargs.get("category_slug")
        
        # параметры для фильтров
        on_sale: str | None = self.request.GET.get("on_sale")
        order_by: str | None = self.request.GET.get("order_by")
        self.query: str | None = self.request.GET.get("q")
        cost_1k: str | None = self.request.GET.get("cost_1k")
        cost_10k: str | None = self.request.GET.get("cost_10k")
        cost_100k: str | None = self.request.GET.get("cost_100k")
        cost_1m: str | None = self.request.GET.get("cost_1m")
        cost_10m: str | None = self.request.GET.get("cost_10m")

        # создается базовый запрос к БД (QuerySet)
        if self.category_slug == "vse-tovary":
            goods: QuerySet[Any] = super().get_queryset()
            
        elif self.query:
            goods = q_search(self.query)

        else:
            goods = super().get_queryset().filter(category__slug=self.category_slug)

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
        
        self.amount = len(goods)
        
        return goods
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        
        # контекстные переменные при поиске
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - Каталог - Поиск"
        context["check_page"] = "MultiShop - Категории"
        context["amount"] = self.amount

        # если не поиск, то добавляются переменные
        if not self.query:
            category = Categories.objects.get(slug=self.category_slug)
            context["title"] = category.name
            context["slug_url"] = self.category_slug
            context["category"] = category
        
        return context


class ProductView(DetailView):
    
    # model = Products
    # slug_field = "slug"
    template_name = "goods/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"
    
    # переопределение model = Products
    def get_object(self, queryset=None) -> Products:
        
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        context["check_page"] = "MultiShop - Продукты"
        return context
