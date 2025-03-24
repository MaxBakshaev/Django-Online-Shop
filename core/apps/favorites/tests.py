from django.test import TestCase


class TestFavorites(TestCase):
    
    def test_favorites_list(self):
        response = self.client.get('/favorites_list/')
        self.assertEqual(response.status_code, 200)
