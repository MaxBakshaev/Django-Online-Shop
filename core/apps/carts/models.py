'''Хранение заказанных товаров в базе данных'''

from typing import Any
from django.db import models

from goods.models import Products
from users.models import User


class CartQueryset(models.QuerySet):
    
    # суммарная цена всех корзин пользователя
    def total_price(self) -> int:
        return sum(cart.products_price() for cart in self)

    # количество всех товаров
    def total_quantity(self) -> int:
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    
    # on_delete=models.CASCADE - если пользователь или продукт удалены, то удаляется и корзина
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key= models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        ordering = ("id",)
        
    objects = CartQueryset().as_manager()    
        
    def products_price(self) -> Any:
        return round(self.product.sell_price() * self.quantity, 0)
      
    def __str__(self) -> str:
        if self.user:
            return f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'
        
        return f'Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}'
