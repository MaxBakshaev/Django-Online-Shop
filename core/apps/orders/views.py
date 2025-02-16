from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch
from django.forms import ValidationError
from django.shortcuts import redirect, render

from carts.models import Cart
from orders.models import Order, OrderItem
from orders.forms import CreateOrderForm


@login_required
def create_order(request):
    
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)
                    
                    if cart_items.exists():
                        # Создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        
                        # Создать заказанные товары
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity
                            
                            if product.quantity < quantity:
                                raise ValidationError(f'Недостаточное количество товара {name} на складе.\
                                    В наличии - {product.quantity}')

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )            
                            product.quantity -= quantity
                            product.save()
                            
                        # Очистить корзину пользователя после создания заказа
                        cart_items.delete()
                            
                        messages.success(request, 'Заказ оформлен!')
                        return redirect('user:profile')
            except ValidationError:
                messages.success(request, f'Недостаточное количество товара {name} на складе.\
                                    В наличии - {product.quantity}')
                return redirect('orders:create_order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            }
        
        form = CreateOrderForm(initial=initial)
    
    context = {
        'title': 'MultiShop - Оформление заказа',
        'form': form,
        'order': True,
    }
    return render(request, 'orders/create_order.html', context=context)
    
def my_orders(request):
    
    orders = (
        Order.objects.filter(user=request.user)
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
            .order_by("-id")
        )
    
    context = {
        'title': 'MultiShop - Заказы',
        'orders': orders,
    }
    return render(request, 'orders/my_orders.html', context=context)

# created_timestamp, id, name, order, order_id, price, product, product_id, quantity