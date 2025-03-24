from django.test import TestCase

from goods.models import Categories, Products


class TestGoods(TestCase):
    
    def test_search(self):
        response = self.client.get('/catalog/search/?q=стол/')
        self.assertEqual(response.status_code, 200)
        
    def test_category(self):
        Categories.objects.create(name='Книги', slug='knigi')
        response = self.client.get('/catalog/knigi/')
        self.assertEqual(response.status_code, 200)
        
    def test_product(self):
        Categories.objects.create(name='Автомобили', slug='avtomobili', id=1)
        Products.objects.create(name='Лимузин', slug='limuzin', price=100, discount=10, quantity=10, category_id=1)
        response = self.client.get('/catalog/product/limuzin/')
        self.assertEqual(response.status_code, 200)
