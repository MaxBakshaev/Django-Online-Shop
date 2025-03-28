from django.urls import path

from favorites import views


app_name = 'favorites'

urlpatterns = [
    path('favorites_list/', views.FavoritesListView.as_view(), name='favorites_list'),
    path('add_to_favorites/', views.AddToFavoritesView.as_view(), name='add_to_favorites'),
    path('<id>/remove_from_favorites/', views.RemoveFromFavoritesView.as_view(), name='remove_from_favorites'),
    # path('delete_favorites/', views.delete_favorites, name='delete_favorites'),
]