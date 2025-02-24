from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch
from django.forms import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from carts.models import Cart
from orders.models import Order, OrderItem
from orders.forms import CreateOrderForm


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = "orders/create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy("users:profile")

    def get_initial(self):
        initial = super().get_initial()
        initial["first_name"] = self.request.user.first_name
        initial["last_name"] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():
                    # Создать заказ
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data["phone_number"],
                        requires_delivery=form.cleaned_data["requires_delivery"],
                        delivery_address=form.cleaned_data["delivery_address"],
                        payment_on_get=form.cleaned_data["payment_on_get"],
                    )

                    # Создать заказанные товары
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        price = cart_item.product.sell_price()
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(
                                f"Недостаточное количество товара {name} на складе.\
                                В наличии - {product.quantity}"
                            )

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        product.quantity -= quantity
                        product.save()

                    # Очистить корзину пользователя после создания заказа
                    cart_items.delete()

                    messages.success(self.request, "Заказ оформлен!")
                    return redirect("user:profile")

        except ValidationError:
            messages.success(
                self.request,
                f"Недостаточное количество товара {name} на складе.\
                                В наличии - {product.quantity}",
            )
            return redirect("orders:create_order")

    def form_invalid(self, form):
        messages.error(self.request, "Заполните все обязательные поля!")
        return redirect("orders:create_order")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Оформление заказа"
        context["order"] = True
        return context


class MyOrdersView(TemplateView):
    template_name = "orders/my_orders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - Заказы"
        context["orders"] = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
            .order_by("-id")
        )
        return context


# @login_required
# def create_order(request):

#     if request.method == "POST":
#         form = CreateOrderForm(data=request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     user = request.user
#                     cart_items = Cart.objects.filter(user=user)

#                     if cart_items.exists():
#                         # Создать заказ
#                         order = Order.objects.create(
#                             user=user,
#                             phone_number=form.cleaned_data["phone_number"],
#                             requires_delivery=form.cleaned_data["requires_delivery"],
#                             delivery_address=form.cleaned_data["delivery_address"],
#                             payment_on_get=form.cleaned_data["payment_on_get"],
#                         )

#                         # Создать заказанные товары
#                         for cart_item in cart_items:
#                             product = cart_item.product
#                             name = cart_item.product.name
#                             price = cart_item.product.sell_price()
#                             quantity = cart_item.quantity

#                             if product.quantity < quantity:
#                                 raise ValidationError(
#                                     f"Недостаточное количество товара {name} на складе.\
#                                     В наличии - {product.quantity}"
#                                 )

#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 price=price,
#                                 quantity=quantity,
#                             )
#                             product.quantity -= quantity
#                             product.save()

#                         # Очистить корзину пользователя после создания заказа
#                         cart_items.delete()

#                         messages.success(request, "Заказ оформлен!")
#                         return redirect("user:profile")
#             except ValidationError:
#                 messages.success(
#                     request,
#                     f"Недостаточное количество товара {name} на складе.\
#                                     В наличии - {product.quantity}",
#                 )
#                 return redirect("orders:create_order")
#     else:
#         initial = {
#             "first_name": request.user.first_name,
#             "last_name": request.user.last_name,
#         }

#         form = CreateOrderForm(initial=initial)

#     context = {
#         "title": "MultiShop - Оформление заказа",
#         "form": form,
#         "order": True,
#     }
#     return render(request, "orders/create_order.html", context=context)


# def my_orders(request):

#     orders = (
#         Order.objects.filter(user=request.user)
#         .prefetch_related(
#             Prefetch(
#                 "orderitem_set",
#                 queryset=OrderItem.objects.select_related("product"),
#             )
#         )
#         .order_by("-id")
#     )

#     context = {
#         "title": "MultiShop - Заказы",
#         "orders": orders,
#     }
#     return render(request, "orders/my_orders.html", context=context)


# created_timestamp, id, name, order, order_id, price, product, product_id, quantity
