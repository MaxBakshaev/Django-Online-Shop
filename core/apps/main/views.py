from typing import Any
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView

from common.mixins import CacheMixin
from core.project.settings import EMAIL_HOST_USER
from main.forms import SendEmailForm
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

    def get_special_product_1(self):
        return Products.objects.get(slug="shipcy-dlya-otzhima-chajnyh-paketikov")

    def get_special_product_2(self):
        return Products.objects.get(slug="griva-dlya-sobaki")

    def get_special_product_3(self):
        return Products.objects.get(slug="betmobil")

    def get_special_product_4(self):
        return Products.objects.get(slug="yahta-eclipse")

    def get_special_product_5(self):
        return Products.objects.get(slug="peel-p50")

    def get_special_product_6(self):
        return Products.objects.get(slug="sebring-vanguard-citicar")

    def get_special_product_7(self):
        return Products.objects.get(slug="tango-t600")

    def get_popular_products_list(self) -> list[tuple]:
        """Возвращает список из 4 продуктов с самой большой скидкой"""
        self.goods = Products.objects.all()
        all_products_list = self.get_products_list()
        most_popular_products = reversed(
            (sorted(all_products_list, key=lambda x: x[1][2]))[-4:]
        )
        return most_popular_products

    def get_discount_products_list(self) -> list[tuple]:
        """Возвращает список из 4 продуктов с самой большой скидкой"""
        self.goods = ((Products.objects.all()).filter(discount__gt=0)).order_by(
            "-discount"
        )[:4]
        return self.get_products_list()

    def get_new_products_list(self) -> list[tuple]:
        """Возвращает список из 4 самых новых продуктов"""
        self.goods = Products.objects.all().order_by("-id")[:4]
        return self.get_products_list()

    def get_context_data(self, **kwargs) -> dict[str, Any]:

        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - Главная"
        context["popular_products"] = self.get_popular_products_list()
        context["discount_products"] = self.get_discount_products_list()
        context["new_products"] = self.get_new_products_list()
        context["special_product_1"] = self.get_special_product_1()
        context["special_product_2"] = self.get_special_product_2()
        context["special_product_3"] = self.get_special_product_3()
        context["special_product_4"] = self.get_special_product_4()
        context["special_product_5"] = self.get_special_product_5()
        context["special_product_6"] = self.get_special_product_6()
        context["special_product_7"] = self.get_special_product_7()

        return context


class AboutView(TemplateView, SendEmailForm, FormView):

    template_name = "main/about.html"
    form_class = SendEmailForm

    def get_success_url(self) -> str:
        """Возвращает URL для перенаправления на эту же страницу"""
        return self.request.path

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            user_email = form.cleaned_data["user_email"]
            user_subject = form.cleaned_data["user_subject"]
            user_message: str = (
                "Тема: {subject}\n\nИмя: {name}\n\nПочта: {email}\n\n{message}".format(
                    subject=user_subject,
                    name=user_name,
                    email=user_email,
                    message=form.cleaned_data["user_message"],
                )
            )

            send_mail(user_subject, user_message, EMAIL_HOST_USER, [EMAIL_HOST_USER])

            messages.success(self.request, "Сообщение отправлено!")
        else:
            form = SendEmailForm()

        return super().form_valid(form)

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
