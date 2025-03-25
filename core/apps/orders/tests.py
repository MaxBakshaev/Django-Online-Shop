from django.test import TestCase

from users.models import User


class TestOrders(TestCase):
    
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        
    def test_redirect_if_user_not_logged(self):
        
        response1 = self.client.get('/orders/create-order/')
        self.assertEqual(response1.status_code, 302)
        self.assertRedirects(response1, '/user/login/?next=/orders/create-order/')
        
        response2 = self.client.get('/orders/my-orders/')
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, '/user/login/?next=/orders/my-orders/')
        
    def test_user_is_logged(self):
        
        login = self.client.login(username='testuser1', password='12345')
        
        response1 = self.client.get('/orders/create-order/')
        self.assertEqual(response1.status_code, 200)
        self.assertTemplateUsed(response1, 'orders/create_order.html')
        
        response2 = self.client.get('/orders/my-orders/')
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'orders/my_orders.html')