from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from common.mixins import CacheMixin
from goods.models import Products


class IndexView(TemplateView, CacheMixin):
    
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)           
        context['title'] = 'MultiShop - Главная' 
        # лучшие скидки
        discount_products = ((Products.objects.all()).filter(discount__gt=0)).order_by('-discount')[:4]
        context["discount_products"] = self.set_get_cache(discount_products, f"user_{self.request.user.id}_discount_products", 600)
        # новинки
        new_products = Products.objects.all().order_by('-id')[:4]
        context["new_products"] = self.set_get_cache(new_products, f"user_{self.request.user.id}_new_products", 600)
        

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
