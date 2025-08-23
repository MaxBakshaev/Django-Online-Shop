# Шаблонные теги

from django import template
from django.utils.http import urlencode

from goods.models import Categories


register = template.Library()


# В шаблоне вызывается функция tag_categories со списком категории товаров
@register.simple_tag()
def tag_categories():
    return Categories.objects.all()


# takes_context=True означает, что все контекстные переменные (из views) будут доступны через context
@register.simple_tag(takes_context=True)
def change_params(context, **kwargs) -> str:
    # получаем параметры GET-запроса, с которыми была открыта страница
    query = context["request"].GET.dict()
    # в словарь добавляются данные какую страницу нужно открыть
    query.update(kwargs)
    # из словаря возвращаются параметры в виде строки для URL-адреса
    return urlencode(query)
