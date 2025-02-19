from django.urls import path

from orders import views


app_name = 'orders'

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
