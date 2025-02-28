from typing import Any
from django.views.generic import TemplateView

from common.mixins import CacheMixin
from goods.models import Products, Review


class IndexView(TemplateView, CacheMixin):
    
    template_name = 'main/index.html'
    
    def get_product_rating(self, new_product_rating):
        return new_product_rating.pop(0)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        
        context: dict[str, Any] = super().get_context_data(**kwargs)           
        context['title'] = 'MultiShop - Главная' 
        # лучшие скидки
        discount_products = ((Products.objects.all()).filter(discount__gt=0)).order_by('-discount')[:4]
        context["discount_products"] = self.set_get_cache(discount_products, f"user_{self.request.user.id}_discount_products", 600)
        
        # новинки
        new_products = Products.objects.all().order_by('-id')[:4]
        context["new_products"] = self.set_get_cache(new_products, f"user_{self.request.user.id}_new_products", 600)
        
        new_product_rating = []
        amount_reviews_list = []
        
        for new_product in new_products:
            reviews = new_product.reviews.all()
            amount_reviews: int = len(reviews)
            amount_reviews_list.append(amount_reviews)
            
            rate = 0
            for review in reviews:
                rate += review.rating
            try:
                product_rating = rate/amount_reviews
            except ZeroDivisionError:
                product_rating = 0
                
            new_product_rating.append(product_rating)
        
        dict_product_rating = dict(zip(new_products, new_product_rating))
        context["dict_product_rating"] = dict_product_rating

        return context


class AboutView(TemplateView):
    
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        
        context: dict[str, Any] = super().get_context_data(**kwargs)           
        context['title'] = 'MultiShop - О нас'
        context['content'] = 'MultiShop - Товары на все случаи жизни'
        context['text_on_page'] = 'Лучший магазин во вселенной'
        
        return context


class All_categories(TemplateView):
    
    template_name = 'main/all_categories.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        
        context: dict[str, Any] = super().get_context_data(**kwargs)           
        context['title'] = 'MultiShop - Каталог'
        
        return context
