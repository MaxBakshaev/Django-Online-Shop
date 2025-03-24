from django.test import TestCase


class TestUsers(TestCase):
    
    def test_login(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_registration(self):
        response = self.client.get('/user/registration/')
        self.assertEqual(response.status_code, 200)
    
    def test_users_password_reset(self):
        response = self.client.get('/user/password-reset/')
        self.assertEqual(response.status_code, 200)
        
    def test_users_password_reset_done(self):
        response = self.client.get('/user/password-reset/done/')
        self.assertEqual(response.status_code, 200)
        
    def test_users_password_reset_complete(self):
        response = self.client.get('/user/password-reset/complete/')
        self.assertEqual(response.status_code, 200)
        
    def test_users_profile(self):
        response = self.client.get('/user/profile/')
        self.assertEqual(response.status_code, 302)
        
    def test_users_cart(self):
        response = self.client.get('/user/users-cart/')
        self.assertEqual(response.status_code, 200)
        
    def test_users_logout(self):
        response = self.client.get('/user/logout/')
        self.assertEqual(response.status_code, 302)
