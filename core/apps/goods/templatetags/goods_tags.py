# Шаблонные теги

from django import template
from django.utils.http import urlencode

from goods.models import Categories


register = template.Library()


# В шаблоне вызывается функция tag_categories со списком категории товаров
@register.simple_tag()
def tag_categories():
    return Categories.objects.all()
