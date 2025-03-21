from typing import Any
from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
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
    

def add_to_favorites(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    if request.method == 'POST':
        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
            request.session['favorites'] = list(request.session['favorites'])
        
        item_exist = next((item for item in request.session['favorites'] if item["type"] == request.POST.get('type') and item["id"] == id), False)
    
        add_data = {
            'type': request.POST.get('type'),
            'id': id,
        }
        
        if not item_exist:
            request.session['favorites'].append(add_data)
            request.session.modified = True
    
        messages.success(request, "Товар добавлен в избранное")
    return redirect(request.POST.get('url_from'))


def remove_from_favorites(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    if request.method == 'POST':
        
        for item in request.session['favorites']:
            if item['id'] == id and item['type'] == request.POST.get('type'):
                item.clear()
                
        while {} in request.session['favorites']:
            request.session['favorites'].remove({})
            
        if not request.session['favorites']:
            del request.session['favorites']
            
        request.session.modified = True
        messages.success(request, "Товар удален из избранного")
    return redirect(request.POST.get('url_from'))


def delete_favorites(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    if request.session.get('favorites'):
        del request.session['favorites']
    return redirect(request.POST.get('url_from'))

    

# def favorite_add(request):
    
#     product_id = request.POST.get("product_id")
#     product = Products.objects.get(id=product_id)
    
#     # Проверка корзины пользователя в БД
#     if request.user.is_authenticated:
#         favorites = Favorite.objects.filter(user=request.user, product=product)

#         if favorites.exists():
#             ...
#         else:
#             Favorite.objects.create(user=request.user, product=product)
   
#     else:
#         favorites = Favorite.objects.filter(
#             session_key=request.session.session_key, product=product)
        
#         if favorites.exists():
#             favorite = favorites.first()
#             if favorite:
#                 ...
#         else:
#             Favorite.objects.create(
#                 session_key=request.session.session_key, product=product)
    
#     user_favorite = get_user_favorites(request)
#     favorite_items_html = render_to_string(
#         "favorites.html", {"favorites": user_favorite}, request=request
#     )
    
#     response_data = {
#         "message": "Товар добавлен в избранное",
#         "favorite_items_html": favorite_items_html,
#     }
    
#     return JsonResponse(response_data)

    
# def favorite_remove(request):
    
#     favorite_id = request.POST.get("favorite_id")
    
#     favorite = Favorite.objects.get(id=favorite_id)
#     favorite.delete()
    
#     user_favorite = get_user_favorites(request)
#     favorite_items_html = render_to_string(
#         "favorites.html", {"favorites": user_favorite}, request=request)
    
#     response_data = {
#         "message": "Товар удален из избранного",
#         "favorite_items_html": favorite_items_html,
#     }
       
#     return JsonResponse(response_data)

