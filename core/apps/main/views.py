from typing import Any
from django.views.generic import TemplateView

from common.mixins import CacheMixin
from goods.mixins import GoodsMixin
from goods.models import Products


class IndexView(TemplateView, CacheMixin, GoodsMixin):
    """
    Обозначение параметров продукта в шаблоне (for discount_product in new_products), (for new_product in new_products):
    discount_product.0, new_product.0 - продукт (объект из queryset)
    discount_product.1.0, new_product.1.0 - оценка
    discount_product.1.1, new_product.1.1 - количество отзывов
    """

    template_name = "main/index.html"
    
    def get_discount_products_list(self) -> list[tuple]:
        """ Возвращает список из 4 продуктов с самой большой скидкой """
        self.goods = ((Products.objects.all()).filter(discount__gt=0)).order_by("-discount")[:4]
        return self.get_products_list()
    
    def get_new_products_list(self) -> list[tuple]:
        """ Возвращает список из 4 самых новых продуктов """
        self.goods = Products.objects.all().order_by("-id")[:4]
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
