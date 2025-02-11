from django.urls import path

from favorites import views


app_name = 'favorites'

urlpatterns = [
    path('favorites_list/', views.favorites_list, name='favorites_list'),
    path('<id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('<id>/remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('delete_favorites/', views.delete_favorites, name='delete_favorites'),
]