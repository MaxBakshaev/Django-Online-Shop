from django.db import models

from users.models import User


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
    
    # метод для названия категории в админке
    def __str__(self) -> str:
        return self.name


class Products(models.Model):  
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    # max_digits и decimal_places - количество знаков до и после запятой
    price = models.DecimalField(default=0, max_digits=20, decimal_places=0, verbose_name='Цена')
    discount = models.DecimalField(default=0, max_digits=20, decimal_places=0, verbose_name='Скидка в %')
    # PositiveIntegerField не может содержать отрицательное чисто в отличие от IntegerField
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    # ForeignKey связывает записи из таблицы Product с таблицей Categories
    # on_delete указывает что делать со всеми связанными товарами при удалении категории (PROTECT, CASCADE, SET_DEFAULT)
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория') 

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        # стандартная сортировка по какому полю
        ordering = ("id",)

    # метод для отображения количества в админке
    def __str__(self) -> str:
        return f'{self.name} Количество - {self.quantity}'
    
    # метод для отображения id с количеством знаков
    def display_id(self) -> str:
        return f'{self.id:05}'
    
    # метод для отображения стоимости товара с учетом скидки
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100, 0)
        
        return self.price
    
    def price_str(self):
        # Преобразует число в строку
        number_str = str(self.price)
        # Разделяет строку на части по три цифры с конца
        parts = []
        while len(number_str) > 3:
            parts.append(number_str[-3:])
            number_str = number_str[:-3]
        if number_str:
            parts.append(number_str)
        # Объединяет части в обратном порядке с пробелами
        return ' '.join(reversed(parts))
    
    def sell_price_str(self):
        if self.discount:
            # Преобразует число в строку
            number_str = str(round(self.price - self.price*self.discount/100, 0))
        else:
            number_str = str(self.price)
            
        # Разделяет строку на части по три цифры с конца
        parts = []
        while len(number_str) > 3:
            parts.append(number_str[-3:])
            number_str = number_str[:-3]
        if number_str:
            parts.append(number_str)
        # Объединяет части в обратном порядке с пробелами
        return ' '.join(reversed(parts))
    
    
class Review(models.Model):
    product = models.ForeignKey(Products, related_name='reviews', on_delete=models.CASCADE, verbose_name='Продукт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Оценка')
    # user_full_name = models.CharField(max_length=150, blank=True)
    comment = models.TextField(blank=True, null=True, verbose_name='Ваш отзыв*')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    # updated = models.DateTimeField(auto_now=True)
    # active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('created',)

    def __str__(self):
        return f'Review by {self.user} for {self.product.name}'
