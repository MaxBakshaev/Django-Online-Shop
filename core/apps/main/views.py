from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from goods.models import Products


class IndexView(TemplateView):
    
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)           
        context['title'] = 'MultiShop - Главная' 
        # лучшие скидки
        context['discount_products'] = ((Products.objects.all()).filter(discount__gt=0)).order_by('-discount')[:4]
        # новинки
        context['new_products'] = Products.objects.all().order_by('-id')[:4]

        return context


class AboutView(TemplateView):
    
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)           
        context['title'] = 'MultiShop - О нас'
        context['content'] = 'MultiShop - Товары на все случаи жизни'
        context['text_on_page'] = 'Лучший магазин во вселенной'
        
        return context


class All_categories(TemplateView):
    
    template_name = 'main/all_categories.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)           
        context['title'] = 'MultiShop - Каталог'
        
        return context
