from typing import Any, Literal
from django.views.generic import TemplateView

from common.mixins import CacheMixin
from goods.models import Products


class IndexView(TemplateView, CacheMixin):
    """
    Обозначение параметров продукта в шаблоне (for discount_product in new_products), (for new_product in new_products):
    discount_product.0, new_product.0 - продукт (объект из queryset)
    discount_product.1.0, new_product.1.0 - оценка
    discount_product.1.1, new_product.1.1 - количество отзывов
    """

    template_name = "main/index.html"

    def get_queryset_discount_products(self):
        """ queryset из 4 товаров по скидке """
        return ((Products.objects.all()).filter(discount__gt=0)).order_by("-discount")[:4]
    
    def get_queryset_new_products(self):
        """ queryset из 4 новых товаров """
        return Products.objects.all().order_by("-id")[:4]

    def get_reviews_ending(self) -> Literal["отзыв"] | Literal["отзыва"] | Literal["отзывов"]:
        """Возвращает слово 'отзыв' в правильном падеже."""
        last_number_of_amount = (str(self.amount_reviews))[len(str(self.amount_reviews)) - 1]
        if last_number_of_amount == "1" and str(self.amount_reviews) != "11":
            reviews_ending = "отзыв"
        elif last_number_of_amount in ["2", "3", "4"] and str(self.amount_reviews) not in ["12", "13", "14"]:
            reviews_ending = "отзыва"
        else:
            reviews_ending = "отзывов"
        return reviews_ending

    def get_product_rating(self):
        """ Возвращает оценку продукта """
        rate = 0
        for review in self.reviews:
            rate += review.rating
        try:
            rating = rate / self.amount_reviews
        except ZeroDivisionError:
            rating = 0
        return rating
    
    def get_products_list(self) -> list[tuple]:
        """ 
        Возвращает список товаров, где элементы:
        Первый кортеж - продукт (объект из queryset)
        Второй кортеж - оценка и количество отзывов о продукте
        """

        # список оценок продуктов
        goods_rating_list = []
        # список количества отзывов продуктов
        goods_amount_reviews_list = []

        for product in self.goods:

            # получение количества отзывов о продуктах и слово "отзыв" в правильном падеже
            self.reviews = product.reviews.all()
            self.amount_reviews: int = len(self.reviews)
            reviews_ending = self.get_reviews_ending()
            goods_amount_reviews_list.append(f"{self.amount_reviews} {reviews_ending}")

            # получение оценки продуктов
            rating = self.get_product_rating()
            goods_rating_list.append(rating)

        dict_product_rating_amount_reviews = {}
        dp_index = 0
        for good in self.goods:
            dict_product_rating_amount_reviews[self.goods[dp_index]] = (
                goods_rating_list[dp_index],
                goods_amount_reviews_list[dp_index],
            )
            dp_index += 1
        return list(dict_product_rating_amount_reviews.items())
    
    def get_discount_products_list(self):
        """ Возвращает список продуктов по скидке """
        self.goods = self.get_queryset_discount_products()
        return self.get_products_list()
    
    def get_new_products_list(self):
        """ Возвращает список новых продуктов """
        self.goods = self.get_queryset_new_products()
        return self.get_products_list()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - Главная"
        context["discount_products"] = self.get_discount_products_list()
        context["new_products"] = self.get_new_products_list()
        
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
