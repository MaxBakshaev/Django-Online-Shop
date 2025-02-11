# '''Хранение избранных товаров в базе данных'''

# from django.db import models

# from goods.models import Products
# from users.models import User


# class Favorite(models.Model):
    
#     # on_delete=models.CASCADE - если пользователь или продукт удалены, то удаляется и корзина
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
#     product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
#     session_key= models.CharField(max_length=32, null=True, blank=True)
#     created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
#     class Meta:
#         db_table = 'favorite'
#         verbose_name = 'Избранное'
#         verbose_name_plural = 'Избранное'
      
#     def __str__(self):
#         if self.user:
#             return f'Избранное {self.user.username} | Товар {self.product.name}'
        
#         return f'Анонимное избранное | Товар {self.product.name}'
