from typing import Any
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import AnonymousUser
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    # succes_url = reverse_lazy('main:index')

    def get_success_url(self) -> str | Any:
        redirect_page: str | None = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse("user:logout"):
            return redirect_page
        return reverse_lazy("main:index")

    def form_valid(self, form) -> HttpResponseRedirect | None:
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)

            # переброска корзины от неавторизованного к авторизованному пользователю
            if session_key:
                # удалить старые авторизованные пользовательские корзины
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                # добавить новую авторизированную корзину пользователя из анонимной сессии
                Cart.objects.filter(session_key=session_key).update(user=user)

                messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")

                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - Авторизация"
        return context


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form) -> HttpResponseRedirect:
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(
            self.request,
            f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт",
        )

        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - Регистрация"
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None) -> AbstractBaseUser | AnonymousUser:
        return self.request.user

    def form_valid(self, form) -> HttpResponse:
        messages.success(self.request, "Профиль успешно обновлен")
        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponse:
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - Кабинет"

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


class UserCartView(TemplateView):
    template_name = "users/users-cart.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "MultiShop - Корзина"
        return context


@login_required
def logout(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect:

    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse("main:index"))


# def login(request):

#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)

#             session_key = request.session.session_key

#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f"{username}, Вы вошли в аккаунт")

#                 # переброска корзина от неавторизованного к авторизованному пользователю
#                 # по сессионному ключу
#                 if session_key:
#                     # удалить старые авторизованные пользовательские корзины
#                     forgot_carts = Cart.objects.filter(user=user)
#                     if forgot_carts.exists():
#                         forgot_carts.delete()
#                     # добавить новую авторизированную корзину пользователя из анонимной сессии
#                     Cart.objects.filter(session_key=session_key).update(user=user)

#                 redirect_page = request.POST.get('next', None)
#                 if redirect_page and redirect_page != reverse('user:logout'):
#                     return HttpResponseRedirect(request.POST.get('next'))

#                 return HttpResponseRedirect(reverse('main:index'))

#     else:
#         form = UserLoginForm()

#     context = {
#         'title': 'MultiShop - Авторизация',
#         'form': form
#     }
#     return render(request, 'users/login.html', context)


# def registration(request):

#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()

#             session_key = request.session.session_key

#             user = form.instance
#             # после успешной регистрации пользователь автоматически авторизируется
#             auth.login(request, user)

#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)

#             messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")

#             return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = UserRegistrationForm()

#     context = {
#         'title': 'MultiShop - Регистрация',
#         'form': form
#     }
#     return render(request, 'users/registration.html', context)


# @login_required проверяет, что если пользователь не авторизован, то возвращает 404 url-страницы user/profile
# @login_required
# def profile(request):

#     if request.method == 'POST':
#         form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Профиль успешно обновлен")

#             return HttpResponseRedirect(reverse('user:profile'))
#     else:
#         form = ProfileForm(instance=request.user)

#     orders = (
#         Order.objects.filter(user=request.user)
#             .prefetch_related(
#                 Prefetch(
#                     "orderitem_set",
#                     queryset=OrderItem.objects.select_related("product"),
#                 )
#             )
#             .order_by("-id")
#         )

#     context = {
#         'title': 'MultiShop - Кабинет',
#         'form': form,
#         'orders': orders,
#     }

#     return render(request, 'users/profile.html', context)


# def users_cart(request):

#     context = {
#         'title': 'MultiShop - Корзина',
#     }

#     return render(request, 'users/users-cart.html', context)
