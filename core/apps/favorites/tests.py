from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse


class TestFavorites(TestCase):

    def setUp(self):
        self.url_add = reverse("favorites:add_to_favorites")
        self.url_remove_id_1 = reverse("favorites:remove_from_favorites", args=[1])
        self.url_remove_id_2 = reverse("favorites:remove_from_favorites", args=[2])
        self.client.post(self.url_add, {"id": "1", "url_from": "/"})
        self.client.post(self.url_add, {"id": "2", "url_from": "/"})

    def test_favorites_list(self):
        response = self.client.get("/favorites_list/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favorites/favorites-list.html")

    def test_add_to_favorites(self):
        response = self.client.post(self.url_add, {"id": "3", "url_from": "/"})
        self.assertEqual(response.status_code, 302)
        self.assertIn({"id": "1"}, self.client.session["favorites"])
        self.assertEqual(self.client.session["favorites"][2]["id"], "3")

    def test_add_existing_to_favorites(self):
        response = self.client.post(self.url_add, {"id": "1", "url_from": "/"})
        self.assertEqual(response.status_code, 302)
        self.assertIn({"id": "1"}, self.client.session["favorites"])
        self.assertEqual(len(self.client.session["favorites"]), 2)

    def test_ajax_add_to_favorites(self):
        request = self.client.post(
            self.url_add,
            {"id": "3"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(request.status_code, 200)
        self.assertIn({"id": "3"}, self.client.session["favorites"])
        self.assertEqual(self.client.session["favorites"][2]["id"], "3")

        response_data = request.json()
        self.assertEqual(response_data["id"], "3")
        self.assertEqual(response_data["message"], "Товар добавлен в избранное")
        self.assertTrue(response_data["success"])

    def test_remove_favorite(self):
        response = self.client.post(self.url_remove_id_1, {"url_from": "/"})
        self.assertEqual(response.status_code, 302)
        self.assertNotIn({"id": "1"}, self.client.session.get("favorites"))
        self.assertIn({"id": "2"}, self.client.session.get("favorites"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Товар удален из избранного")

    def test_non_existing_favorites_after_remove(self):
        self.client.post(self.url_remove_id_1, {"url_from": "/"})
        response = self.client.post(self.url_remove_id_2, {"url_from": "/"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get("favorites"), None)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Товар удален из избранного")
