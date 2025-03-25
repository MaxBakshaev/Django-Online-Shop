from django.test import TestCase

from goods.models import Categories, Products


class TestMain(TestCase):
    
    def setUp(self):
        Categories.objects.create(name='Автомобили', slug='avtomobili', id=1)
        Products.objects.create(name='1', image='1', price=100, discount=10, quantity=10, category_id=1, slug='shipcy-dlya-otzhima-chajnyh-paketikov')
        Products.objects.create(name='2', image='2', price=100, discount=10, quantity=10, category_id=1, slug='griva-dlya-sobaki')
        Products.objects.create(name='3', image='3', price=100, discount=10, quantity=10, category_id=1, slug='betmobil')
        Products.objects.create(name='4', image='4', price=100, discount=10, quantity=10, category_id=1, slug='yahta-eclipse')
        Products.objects.create(name='5', image='5', price=100, discount=10, quantity=10, category_id=1, slug='peel-p50')
        Products.objects.create(name='6', image='6', price=100, discount=10, quantity=10, category_id=1, slug='sebring-vanguard-citicar')
        Products.objects.create(name='7', image='7', price=100, discount=10, quantity=10, category_id=1, slug='tango-t600')
    
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')
        
    def test_about(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')
    
    def test_all_categories(self):
        response = self.client.get('/all_categories/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/all_categories.html')
        
    def test_admin(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/login/?next=/admin/')

