from django.db import models
from django.urls import reverse


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
    
    # метод для названия категории в админке
    def __str__(self):
        return self.name


class Products(models.Model):  
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    # max_digits и decimal_places - количество знаков до и после запятой
    price = models.DecimalField(default=0.00, max_digits=20, decimal_places=0, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=20, decimal_places=0, verbose_name='Скидка в %')
    # PositiveIntegerField не может содержать отрицательное чисто в отличие от IntegerField
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    # ForeignKey связывает записи из таблицы Product с таблицей Categories
    # on_delete указывает что делать со всеми связанными товарами при удалении категории (PROTECT, CASCADE, SET_DEFAULT)
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
    

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    # метод для отображения количества в админке
    def __str__(self):
        return f'{self.name} Количество - {self.quantity}'
    
    # метод для отображения id с количеством знаков
    def display_id(self):
        return f'{self.id:05}'
    
    # метод для отображения стоимости товара с учетом скидки
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100, 0)
        
        return self.price