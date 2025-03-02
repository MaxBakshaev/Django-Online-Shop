from typing import Any
from django.views.generic import TemplateView

from common.mixins import CacheMixin
from goods.models import Products


class IndexView(TemplateView, CacheMixin):

    template_name = "main/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        discount_product - dp
        new_product - np
        
        Обозначение параметров продукта в шаблоне (for discount_product in new_products), (for new_product in new_products):
        discount_product.0, new_product.0 - объект из queryset
        discount_product.1.0, new_product.1.0 - оценка
        discount_product.1.1, new_product.1.1 - количество отзывов
        """

        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - Главная"

        # запрос по 4 продуктам с лучшими скидками
        discount_products = ((Products.objects.all()).filter(discount__gt=0)).order_by("-discount")[:4]
        context["discount_products"] = self.set_get_cache(discount_products, f"user_{self.request.user.id}_discount_products", 600)

        dp_rating_list = []
        dp_amount_reviews_list = []

        for dp in discount_products:

            # получение количества отзывов о продуктах по скидке
            dp_reviews = dp.reviews.all()
            dp_amount_reviews: int = len(dp_reviews)
            
            dp_amount = (str(dp_amount_reviews))[len(str(dp_amount_reviews))-1]
            if dp_amount == '1' and str(dp_amount_reviews) != '11':
                reviews_ending = "отзыв"
            elif dp_amount in ['2', '3', '4'] and str(dp_amount_reviews) not in ['12', '13', '14']:
                reviews_ending = "отзыва"
            else:
                reviews_ending = "отзывов"
            
            dp_amount_reviews_list.append(f'{dp_amount_reviews} {reviews_ending}')

            # получение оценки продуктов по скидке
            dp_rate = 0
            for dp_review in dp_reviews:
                dp_rate += dp_review.rating
            try:
                dp_rating = dp_rate / dp_amount_reviews
            except ZeroDivisionError:
                dp_rating = 0

            dp_rating_list.append(dp_rating)

        dict_discount_product_rating_amount_reviews = {}
        dp_index = 0
        for dp_element in discount_products:
            # в словарь передаются идентификатор продукта - ключ, оценка и количество отзывов - значение
            dict_discount_product_rating_amount_reviews[discount_products[dp_index]] = (
                dp_rating_list[dp_index],
                dp_amount_reviews_list[dp_index],
            )
            dp_index += 1
        
        discount_products = list(dict_discount_product_rating_amount_reviews.items())
            
        context["discount_products"] = discount_products

        # запрос по 4 новым продуктам
        new_products = Products.objects.all().order_by("-id")[:4]
        context["new_products"] = self.set_get_cache(
            new_products, f"user_{self.request.user.id}_new_products", 600
        )

        np_rating_list = []
        np_amount_reviews_list = []

        for np in new_products:

            # получение количества отзывов о новых продуктах
            np_reviews = np.reviews.all()
            np_amount_reviews: int = len(np_reviews)
            
            np_amount = (str(np_amount_reviews))[len(str(np_amount_reviews))-1]
            if np_amount == '1' and str(np_amount_reviews) != '11':
                reviews_ending = "отзыв"
            elif np_amount in ['2', '3', '4'] and str(np_amount_reviews) not in ['12', '13', '14']:
                reviews_ending = "отзыва"
            else:
                reviews_ending = "отзывов"
                
            np_amount_reviews_list.append(f'{np_amount_reviews} {reviews_ending}')

            # получение оценки новых продуктов
            np_rate = 0
            for np_review in np_reviews:
                np_rate += np_review.rating
            try:
                np_rating = np_rate / np_amount_reviews
            except ZeroDivisionError:
                np_rating = 0

            np_rating_list.append(np_rating)

        dict_new_product_rating_amount_reviews = {}
        np_index = 0
        for np_element in new_products:
            # в словарь передаются идентификатор продукта - ключ, оценка и количество отзывов - значение
            dict_new_product_rating_amount_reviews[new_products[np_index]] = (
                np_rating_list[np_index],
                np_amount_reviews_list[np_index],
            )
            np_index += 1
            
        new_products = list(dict_new_product_rating_amount_reviews.items())
            
        context["new_products"] = new_products

        return context


class AboutView(TemplateView):

    template_name = "main/about.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:

        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - О нас"
        context["content"] = "MultiShop - Товары на все случаи жизни"
        context["text_on_page"] = "Лучший магазин во вселенной"

        return context


class All_categories(TemplateView):

    template_name = "main/all_categories.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:

        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - Каталог"

        return context
