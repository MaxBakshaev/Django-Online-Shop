from typing import Any
from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView

from goods.models import Products
from goods.mixins import GoodsMixin

class FavoritesListView(ListView, GoodsMixin):
    """
    Обозначение параметров продукта в шаблоне (for product in goods):
    product.0 - продукт (объект из queryset)
    product.1.0 - оценка
    product.1.1 - количество отзывов
    """
    
    model = Products
    template_name = "favorites/favorites-list.html"
    context_object_name = "goods"
    
    def get_queryset(self) -> QuerySet[Any]:
        if self.request.session.get('favorites'):
            list_id = []
            for item in self.request.session['favorites']:
                product_id = item['id']
                list_id.append(product_id)
            
            self.goods = Products.objects.filter(pk__in=list_id)
            self.amount = len(self.goods)
            goods = self.get_products_list()
            
        else:
            goods = 0
            self.amount = 0

        return goods
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['title'] = 'MultiShop - Избранное'

        return context
    

class AddToFavoritesView(View):
    
    def post(self, request) -> JsonResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:

        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
            request.session['favorites'] = list(request.session['favorites'])
        
        item_id = request.POST.get('id')
        item_exist = next((item for item in request.session['favorites'] if item["id"] == item_id), False)

        add_data = {
            'id': item_id,
        }
        
        if not item_exist:
            request.session['favorites'].append(add_data)
            request.session.modified = True
            message = "Товар добавлен в избранное"
            success = True
        else:
            message = "Товар уже в избранном"
            success = False
        
        if self.is_ajax(request):
            data = {
                'id': item_id,
                'message': message,
                'success': success,
            }
            request.session.modified = True
            return JsonResponse(data)
        
        return redirect(request.POST.get('url_from'))
    
    @staticmethod
    def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        

class RemoveFromFavoritesView(View):
    
    def post(self, request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        if request.method == 'POST':
            
            if 'favorites' in request.session:
                request.session['favorites'] = [item for item in request.session['favorites'] if item.get('id') != id]
            item_id = request.POST.get('id')
            for item in request.session['favorites']:
                if item['id'] == item_id:
                    item.clear()
                
            if not request.session['favorites']:
                del request.session['favorites']
                
            request.session.modified = True
            messages.success(request, "Товар удален из избранного")
            
        return redirect(request.POST.get('url_from'))


# def delete_favorites(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
#     if request.session.get('favorites'):
#         del request.session['favorites']
#     return redirect(request.POST.get('url_from'))
