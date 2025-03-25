from django.test import TestCase

from goods.models import Categories, Products
from users.models import User


class TestUsers(TestCase):
    
    def setUp(self):
        
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        
        Categories.objects.create(name='Автомобили', slug='avtomobili', id=1)
        Products.objects.create(name='1', image='1', price=100, discount=10, quantity=10, category_id=1, slug='shipcy-dlya-otzhima-chajnyh-paketikov')
        Products.objects.create(name='2', image='2', price=100, discount=10, quantity=10, category_id=1, slug='griva-dlya-sobaki')
        Products.objects.create(name='3', image='3', price=100, discount=10, quantity=10, category_id=1, slug='betmobil')
        Products.objects.create(name='4', image='4', price=100, discount=10, quantity=10, category_id=1, slug='yahta-eclipse')
        Products.objects.create(name='5', image='5', price=100, discount=10, quantity=10, category_id=1, slug='peel-p50')
        Products.objects.create(name='6', image='6', price=100, discount=10, quantity=10, category_id=1, slug='sebring-vanguard-citicar')
        Products.objects.create(name='7', image='7', price=100, discount=10, quantity=10, category_id=1, slug='tango-t600')
    
    def users_login(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        
    def users_registration(self):
        response = self.client.get('/user/registration/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
        
    def test_users_password_reset(self):
        response = self.client.get('/user/password-reset/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_reset_form.html')
        
    def test_users_password_reset_done(self):
        response = self.client.get('/user/password-reset/done/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_reset_done.html')
        
    def test_users_password_reset_complete(self):
        response = self.client.get('/user/password-reset/complete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_reset_complete.html')
        
    def test_users_cart(self):
        response = self.client.get('/user/users-cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/users-cart.html')
        
    def test_redirect_if_user_not_logged(self):
         
        response1= self.client.get('/user/profile/')
        self.assertEqual(response1.status_code, 302)
        self.assertRedirects(response1, '/user/login/?next=/user/profile/')
        
        response2 = self.client.get('/user/logout/')
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, '/user/login/?next=/user/logout/')
        
    def test_user_is_logged(self):
        
        login = self.client.login(username='testuser1', password='12345')
        
        response1 = self.client.get('/user/profile/')
        self.assertEqual(str(response1.context['user']), 'testuser1')
        self.assertEqual(response1.status_code, 200)
        self.assertTemplateUsed(response1, 'users/profile.html')

        response2 = self.client.get('/user/logout/')
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, '/')