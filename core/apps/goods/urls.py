from django.urls import path

from goods import views


app_name = 'goods'

urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'), # catalog
    path('product/<slug:product_slug>/', views.product, name='product'),
]
