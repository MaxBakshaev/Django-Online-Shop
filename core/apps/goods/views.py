from typing import Any
from django.contrib import messages
from django.db.models import QuerySet
from django.views.generic import DetailView, FormView, ListView
from django.http import HttpResponse

from goods.forms import CreateReviewForm
from goods.utils import q_search
from goods.mixins import GoodsMixin
from goods.models import Categories, Products


class CatalogView(ListView, GoodsMixin):
    """
    Обозначение параметров продукта в шаблоне (for product in goods):
    product.0 - продукт (объект из queryset)
    product.1.0 - оценка
    product.1.1 - количество отзывов
    """

    model = Products
    # queryset = Products.objects.all()
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 6

    def filter_on_sale(self) -> QuerySet[Any]:
        """Возвращает запрос отфильтрованный по товару со скидкой"""
        if self.on_sale:
            self.goods = self.goods.filter(discount__gt=0)
        return self.goods

    def filter_order(self) -> QuerySet[Any]:
        """Возвращает запрос отфильтрованный по товару в порядке добавления"""
        if self.order_by and self.order_by != "default":
            self.goods = self.goods.order_by(self.order_by)
        return self.goods

    def filter_one_cost(self) -> QuerySet[Any]:
        """Возвращает запрос отфильтрованный по 1 цене"""
        if (
            self.cost_1k
            and not self.cost_10k
            and not self.cost_100k
            and not self.cost_1m
            and not self.cost_10m
        ):
            self.goods = self.goods.filter(price__lt=1_000)
        if (
            self.cost_10k
            and not self.cost_1k
            and not self.cost_100k
            and not self.cost_1m
            and not self.cost_10m
        ):
            self.goods = self.goods.filter(price__lt=10_000, price__gt=1_000)
        if (
            self.cost_100k
            and not self.cost_1k
            and not self.cost_10k
            and not self.cost_1m
            and not self.cost_10m
        ):
            self.goods = self.goods.filter(price__lt=100_000, price__gt=10_000)
        if (
            self.cost_1m
            and not self.cost_1k
            and not self.cost_10k
            and not self.cost_100k
            and not self.cost_10m
        ):
            self.goods = self.goods.filter(price__lt=1_000_000, price__gt=100_000)
        if (
            self.cost_10m
            and not self.cost_1k
            and not self.cost_10k
            and not self.cost_100k
            and not self.cost_1m
        ):
            self.goods = self.goods.filter(price__gt=1_000_000)
        return self.goods

    def filter_two_cost(self) -> QuerySet[Any]:
        """Возвращает запрос отфильтрованный по 2 ценам"""
        if (
            self.cost_1k
            and self.cost_10k
            and not self.cost_100k
            and not self.cost_1m
            and not self.cost_10m
        ):
            self.goods = self.goods.filter(price__lt=10_000)
        if (
            self.cost_10k
            and self.cost_100k
            and not self.cost_1k
            and not self.cost_1m
            and not self.cost_10m
        ):
            self.goods = self.goods.filter(price__lt=100_000, price__gt=1_000)
        if (
            self.cost_100k
            and self.cost_1m
            and not self.cost_1k
            and not self.cost_10k
            and not self.cost_10m
        ):
            self.goods = self.goods.filter(price__lt=1_000_000, price__gt=10_000)
        if (
            self.cost_1m
            and self.cost_10m
            and not self.cost_1k
            and not self.cost_10k
            and not self.cost_100k
        ):
            self.goods = self.goods.filter(price__gt=1_000_000)
        return self.goods

    def filter_three_cost(self) -> QuerySet[Any]:
        """Возвращает запрос отфильтрованный по 3 ценам"""
        if (
            self.cost_1k
            and self.cost_10k
            and self.cost_100k
            and not self.cost_1m
            and not self.cost_10m
        ):
            self.goods = self.goods.filter(price__lt=100_000)
        if (
            self.cost_10k
            and self.cost_100k
            and self.cost_1m
            and not self.cost_1k
            and not self.cost_10m
        ):
            self.goods = self.goods.filter(price__lt=1_000_000, price__gt=1_000)
        if (
            self.cost_100k
            and self.cost_1m
            and self.cost_10m
            and not self.cost_1k
            and not self.cost_10k
        ):
            self.goods = self.goods.filter(price__gt=10_000)
        return self.goods

    def filter_four_cost(self) -> QuerySet[Any]:
        """Возвращает запрос отфильтрованный по 4 ценам"""
        if (
            self.cost_1k
            and self.cost_10k
            and self.cost_100k
            and self.cost_1m
            and not self.cost_10m
        ):
            self.goods = self.goods.filter(price__lt=1_000_000)
        if (
            self.cost_10k
            and self.cost_100k
            and self.cost_1m
            and self.cost_10m
            and not self.cost_1k
        ):
            self.goods = self.goods.filter(price__gt=1_000)
        return self.goods

    def get_queryset(self) -> QuerySet[Any]:

        self.category_slug = self.kwargs.get("category_slug")
        self.query: str | None = self.request.GET.get("q")
        self.on_sale: str | None = self.request.GET.get("on_sale")
        self.order_by: str | None = self.request.GET.get("order_by")
        self.cost_1k: str | None = self.request.GET.get("cost_1k")
        self.cost_10k: str | None = self.request.GET.get("cost_10k")
        self.cost_100k: str | None = self.request.GET.get("cost_100k")
        self.cost_1m: str | None = self.request.GET.get("cost_1m")
        self.cost_10m: str | None = self.request.GET.get("cost_10m")

        if self.category_slug == "vse-tovary":
            self.goods: QuerySet[Any] = super().get_queryset()

        elif self.query:
            self.goods = q_search(self.query)

        else:
            self.goods = (
                super().get_queryset().filter(category__slug=self.category_slug)
            )

        # Проверки с добавлением фильтров к запросу
        goods = self.filter_on_sale()
        goods = self.filter_order()
        goods = self.filter_one_cost()
        goods = self.filter_two_cost()
        goods = self.filter_three_cost()
        goods = self.filter_four_cost()

        # количество товаров
        self.amount = len(self.goods)

        goods = self.get_products_list()

        return goods

    def get_context_data(self, **kwargs) -> dict[str, Any]:

        # контекстные переменные при поиске
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - Каталог - Поиск"
        context["check_page"] = "MultiShop - Категории"
        context["amount"] = self.amount
        context["goods_ending"] = self.get_goods_ending()

        # если не поиск, то добавляются переменные
        if not self.query:
            category = Categories.objects.get(slug=self.category_slug)
            context["title"] = category.name
            context["slug_url"] = self.category_slug
            context["category"] = category

        return context


class ProductView(DetailView, FormView, GoodsMixin):

    template_name = "goods/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"
    form_class = CreateReviewForm

    def get_object(self, queryset=None) -> Products:
        self.product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return self.product

    def get_success_url(self) -> str:
        """Возвращает URL для перенаправления на эту же страницу"""
        return self.request.path

    def form_valid(self, form) -> HttpResponse:
        """Сохраняет отзыв о товаре"""
        if form.is_valid():
            review = form.save(commit=False)
            review.product = self.get_object()
            review.user = self.request.user
            review.save()
            messages.success(self.request, "Отзыв оставлен!")
        else:
            form = CreateReviewForm()

        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        context["check_page"] = "MultiShop - Продукты"

        self.reviews = self.product.reviews.all()
        self.amount_reviews = len(self.reviews)

        context["reviews"] = self.reviews
        context["amount_reviews"] = self.amount_reviews
        context["product_rating"] = self.get_product_rating()
        context["reviews_ending"] = self.get_reviews_ending()

        return context
