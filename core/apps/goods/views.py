from typing import Any
from django.contrib import messages
from django.db.models import QuerySet
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.http import HttpResponse, HttpResponseRedirect

from goods.forms import CreateReviewForm
from goods.utils import q_search
from goods.models import Categories, Products


class CatalogView(ListView):
    """
    Обозначение параметров продукта в шаблоне (for product in goods):
    product.0 - объект из queryset
    product.1.0 - оценка
    product.1.1 - количество отзывов
    """

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
        products_amount = (str(self.amount))[len(str(self.amount))-1]
        if products_amount == '1' and str(self.amount) != '11':
            self.goods_ending = "товар"
        elif products_amount in ['2', '3', '4'] and str(self.amount) not in ['12', '13', '14']:
            self.goods_ending = "товара"
        else:
            self.goods_ending = "товаров"
        
        goods_rating_list = []
        goods_amount_reviews_list = []

        for product in goods:

            # получение количества отзывов о продуктах
            product_reviews = product.reviews.all()
            product_amount_reviews: int = len(product_reviews)
            
            product_amount = (str(product_amount_reviews))[len(str(product_amount_reviews))-1]
            if product_amount == '1' and str(product_amount_reviews) != '11':
                reviews_ending = "отзыв"
            elif product_amount in ['2', '3', '4'] and str(product_amount_reviews) not in ['12', '13', '14']:
                reviews_ending = "отзыва"
            else:
                reviews_ending = "отзывов"
            
            goods_amount_reviews_list.append(f'{product_amount_reviews} {reviews_ending}')

            # получение оценки продуктов
            product_rate = 0
            for product_review in product_reviews:
                product_rate += product_review.rating
            try:
                product_rating = product_rate / product_amount_reviews
            except ZeroDivisionError:
                product_rating = 0

            goods_rating_list.append(product_rating)

        dict_product_rating_amount_reviews = {}
        product_index = 0
        for product_element in goods:
            # в словарь передаются идентификатор продукта - ключ, оценка и количество отзывов - значение
            dict_product_rating_amount_reviews[goods[product_index]] = (
                goods_rating_list[product_index],
                goods_amount_reviews_list[product_index],
            )
            product_index += 1

        goods = list(dict_product_rating_amount_reviews.items())
        
        return goods

    def get_context_data(self, **kwargs) -> dict[str, Any]:

        # контекстные переменные при поиске
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - Каталог - Поиск"
        context["check_page"] = "MultiShop - Категории"
        context["amount"] = self.amount
        context["goods_ending"] = self.goods_ending

        # если не поиск, то добавляются переменные
        if not self.query:
            category = Categories.objects.get(slug=self.category_slug)
            context["title"] = category.name
            context["slug_url"] = self.category_slug
            context["category"] = category

        return context


def product(request, product_slug) -> HttpResponseRedirect | HttpResponse:
    product = Products.objects.get(slug=product_slug)
    reviews = product.reviews.all()
    amount_reviews: int = len(reviews)
    
    rate = 0
    for review in reviews:
        rate += review.rating
    
    try:
        product_rating = rate/amount_reviews
    except ZeroDivisionError:
        product_rating = 0
    
    a = (str(amount_reviews))[len(str(amount_reviews))-1]
    if a == '1' and str(amount_reviews) != '11':
        reviews_ending = "отзыв"
    elif a in ['2', '3', '4'] and str(amount_reviews) not in ['12', '13', '14']:
        reviews_ending = "отзыва"
    else:
        reviews_ending = "отзывов"

    if request.method == "POST":
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Отзыв оставлен!")
            return HttpResponseRedirect(request.path)
    else:
        form = CreateReviewForm()

    return render(
        request,
        "goods/product.html",
        {
            "title": product.name,
            "check_page": "MultiShop - Продукты",
            "product": product,
            "reviews": reviews,
            "form": form,
            "amount_reviews": amount_reviews,
            "product_rating": product_rating,
            "reviews_ending": reviews_ending,
        },
    )


# class CatalogView(ListView):

#     model = Products
#     # queryset = Products.objects.all()
#     template_name = "goods/catalog.html"
#     context_object_name = "goods"
#     paginate_by = 6

#     def get_queryset(self) -> QuerySet[Any]:

#         self.category_slug = self.kwargs.get("category_slug")

#         # параметры для фильтров
#         on_sale: str | None = self.request.GET.get("on_sale")
#         order_by: str | None = self.request.GET.get("order_by")
#         self.query: str | None = self.request.GET.get("q")
#         cost_1k: str | None = self.request.GET.get("cost_1k")
#         cost_10k: str | None = self.request.GET.get("cost_10k")
#         cost_100k: str | None = self.request.GET.get("cost_100k")
#         cost_1m: str | None = self.request.GET.get("cost_1m")
#         cost_10m: str | None = self.request.GET.get("cost_10m")

#         # создается базовый запрос к БД (QuerySet)
#         if self.category_slug == "vse-tovary":
#             goods: QuerySet[Any] = super().get_queryset()

#         elif self.query:
#             goods = q_search(self.query)

#         else:
#             goods = super().get_queryset().filter(category__slug=self.category_slug)

#         # Проверки с добавлением фильтров к запросу
#         if on_sale:
#             goods = goods.filter(discount__gt=0)

#         if order_by and order_by != "default":
#             goods = goods.order_by(order_by)

#         # Eсли выбран 1 параметр цены
#         if cost_1k and not cost_10k and not cost_100k and not cost_1m and not cost_10m:
#             goods = goods.filter(price__lt=1_000)

#         if cost_10k and not cost_1k and not cost_100k and not cost_1m and not cost_10m:
#             goods = goods.filter(price__lt=10_000, price__gt=1_000)

#         if cost_100k and not cost_1k and not cost_10k and not cost_1m and not cost_10m:
#             goods = goods.filter(price__lt=100_000, price__gt=10_000)

#         if cost_1m and not cost_1k and not cost_10k and not cost_100k and not cost_10m:
#             goods = goods.filter(price__lt=1_000_000, price__gt=100_000)

#         if cost_10m and not cost_1k and not cost_10k and not cost_100k and not cost_1m:
#             goods = goods.filter(price__gt=1_000_000)

#         # Eсли выбрано 2 параметра цены
#         if cost_1k and cost_10k and not cost_100k and not cost_1m and not cost_10m:
#             goods = goods.filter(price__lt=10_000)

#         if cost_10k and cost_100k and not cost_1k and not cost_1m and not cost_10m:
#             goods = goods.filter(price__lt=100_000, price__gt=10_000)

#         if cost_100k and cost_1m and not cost_1k and not cost_10k and not cost_10m:
#             goods = goods.filter(price__lt=1_000_000, price__gt=100_000)

#         if cost_1m and cost_10m and not cost_1k and not cost_10k and not cost_100k:
#             goods = goods.filter(price__gt=1_000_000)

#         # Eсли выбрано 3 параметра цены
#         if cost_1k and cost_10k and cost_100k and not cost_1m and not cost_10m:
#             goods = goods.filter(price__lt=100_000)

#         if cost_10k and cost_100k and cost_1m and not cost_1k and not cost_10m:
#             goods = goods.filter(price__lt=1_000_000, price__gt=10_000)

#         if cost_100k and cost_1m and cost_10m and not cost_1k and not cost_10k:
#             goods = goods.filter(price__gt=100_000)

#         # Eсли выбрано 4 параметра цены
#         if cost_1k and cost_10k and cost_100k and cost_1m and not cost_10m:
#             goods = goods.filter(price__lt=1_000_000)

#         if cost_10k and cost_100k and cost_1m and cost_10m and not cost_1k:
#             goods = goods.filter(price__gt=1_000)

#         self.amount = len(goods)

#         goods_rating_list = []
#         goods_amount_reviews_list = []

#         for product in goods:

#             # получение количества отзывов о продуктах
#             product_reviews = product.reviews.all()
#             product_amount_reviews: int = len(product_reviews)
#             goods_amount_reviews_list.append(product_amount_reviews)

#             # получение оценки продуктов
#             product_rate = 0
#             for product_review in product_reviews:
#                 product_rate += product_review.rating
#             try:
#                 product_rating = product_rate / product_amount_reviews
#             except ZeroDivisionError:
#                 product_rating = 0

#             goods_rating_list.append(product_rating)

#         self.dict_product_rating_amount_reviews = {}
#         product_index = 0
#         for product_element in goods:
#             # в словарь передаются идентификатор продукта - ключ, оценка и количество отзывов - значение
#             self.dict_product_rating_amount_reviews[goods[product_index]] = (
#                 goods_rating_list[product_index],
#                 goods_amount_reviews_list[product_index],
#             )
#             product_index += 1

#         return goods

#     def get_context_data(self, **kwargs) -> dict[str, Any]:

#         # контекстные переменные при поиске
#         context: dict[str, Any] = super().get_context_data(**kwargs)
#         context["title"] = "MultiShop - Каталог - Поиск"
#         context["check_page"] = "MultiShop - Категории"
#         context["amount"] = self.amount

#         # если не поиск, то добавляются переменные
#         if not self.query:
#             category = Categories.objects.get(slug=self.category_slug)

#             context["dict_product_rating_amount_reviews"] = (
#                 self.dict_product_rating_amount_reviews
#             )
#             context["title"] = category.name
#             context["slug_url"] = self.category_slug
#             context["category"] = category

#         return context



# class ProductView(DetailView):

#     # model = Products
#     # slug_field = "slug"
#     template_name = "goods/product.html"
#     slug_url_kwarg = "product_slug"
#     context_object_name = "product"

#     # переопределение model = Products
#     def get_object(self, queryset=None) -> Products:

#         product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
#         return product

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

#         context: dict[str, Any] = super().get_context_data(**kwargs)
#         context["title"] = self.object.name
#         context["check_page"] = "MultiShop - Продукты"

#         reviews = Review.objects.filter(post=self.object)
#         context["reviews"] = reviews
#         context["amount_reviews"] = len(reviews)

#         return context


# def create_review(request, product_id):

#     product = Products.objects.get(id=product_id)
#     reviews = product.reviews.all()

#     if request.method == 'POST':
#         form = CreateReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.product = product
#             review.user = request.user
#             review.save()
#             return redirect('product_detail', product_id=product.id)
#     else:
#         form = CreateReviewForm()

#     return render(request, 'goods/product.html', {'product': product, 'reviews': reviews, 'form': form})


# if request.method == 'POST':
#     form = CreateReviewForm(data=request.POST)

# if form.is_valid():
#     try:
#         with transaction.atomic():

#             Comment.objects.create(
# post_name = form.cleaned_data['post_name'],
# user_full_name=f"{self.user.last_name} {self.user.first_name}",
# user_full_name=form.cleaned_data['user_full_name'],
# user_img=form.cleaned_data['user_img'],
# body=form.cleaned_data['body'],
# created=form.cleaned_data['created'],
# updated=form.cleaned_data['updated'],
# active=form.cleaned_data['active'],
#                 )

#                 messages.success(request, 'Обзор накатан!')
#                 return redirect(request.POST.get('url_from'))

#         except ValidationError:
#             messages.success(request, 'Обзор не написать')
#             return redirect(request.POST.get('url_from'))
# else:
#     return redirect(request.POST.get('url_from'))
