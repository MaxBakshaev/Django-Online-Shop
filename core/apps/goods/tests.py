from django.test import TestCase

from goods.models import Categories, Products


class TestGoods(TestCase):
    
    def setUp(self):
        Categories.objects.create(name='Книги', slug='knigi', id=1)
        Categories.objects.create(name='Автомобили', slug='avtomobili', id=2)
        Products.objects.create(name='Лимузин', slug='limuzin', price=100, discount=10, quantity=10, category_id=2)

    def test_search(self):
        response = self.client.get('/catalog/search/?q=стол/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/catalog.html')
        
    def test_category(self):
        response = self.client.get('/catalog/knigi/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/catalog.html')
        
    def test_product(self):
        response = self.client.get('/catalog/product/limuzin/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/product.html')
