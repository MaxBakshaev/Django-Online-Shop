from django.test import TestCase
from django.urls import reverse

from carts.models import Cart
from goods.models import Categories, Products
from users.models import User


class TestOrders(TestCase):

    def setUp(self):
        Categories.objects.create(name="test_category", slug="test-category", id=1)
        self.product = Products.objects.create(
            name="Test Product",
            image="1",
            price=100,
            discount=10,
            quantity=10,
            category_id=1,
            slug="test-product",
        )
        self.test_user1 = User.objects.create_user(
            username="testuser1", password="12345"
        )
        self.test_user1.save()

    def test_cart_add_anonymous_user(self):
        response = self.client.post(
            reverse("carts:cart_add"), {"product_id": self.product.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cart.objects.count(), 1)
        cart = Cart.objects.first()
        self.assertEqual(cart.product, self.product)
        self.assertEqual(cart.quantity, 1)

    def test_cart_add_authenticated_user(self):
        self.client.login(username="testuser1", password="12345")
        response = self.client.post(
            reverse("carts:cart_add"), {"product_id": self.product.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cart.objects.count(), 1)
        cart = Cart.objects.first()

        self.assertEqual(cart.product, self.product)
        self.assertEqual(cart.quantity, 1)
        self.assertEqual(cart.user, self.test_user1)

    def test_increase_product_quantity_in_cart_authenticated_user(self):
        self.client.login(username="testuser1", password="12345")

        self.client.post(reverse("carts:cart_add"), {"product_id": self.product.id})
        self.assertEqual(Cart.objects.count(), 1)

        response = self.client.post(
            reverse("carts:cart_add"), {"product_id": self.product.id}
        )
        self.assertEqual(response.status_code, 200)
        cart = Cart.objects.first()
        self.assertEqual(cart.quantity, 2)

    def test_change_quantity_anonymous_user(self):
        cart = Cart.objects.create(
            user=self.test_user1, product=self.product, quantity=1
        )
        response = self.client.post(
            reverse("carts:cart_change"), {"cart_id": cart.id, "quantity": 5}
        )
        self.assertEqual(response.status_code, 200)
        cart.refresh_from_db()
        self.assertEqual(cart.quantity, 5)

    def test_change_quantity_authenticated_user(self):
        cart = Cart.objects.create(
            user=self.test_user1, product=self.product, quantity=1
        )
        self.client.login(username="testuser1", password="12345")

        response = self.client.post(
            reverse("carts:cart_change"), {"cart_id": cart.id, "quantity": 3}
        )
        self.assertEqual(response.status_code, 200)
        cart.refresh_from_db()
        self.assertEqual(cart.quantity, 3)

    def test_cart_remove_anonymous_user(self):
        Cart.objects.create(user=self.test_user1, product=self.product, quantity=1)

        response = self.client.post(
            reverse("carts:cart_remove"), {"product_id": self.product.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cart.objects.count(), 0)

    def test_cart_remove_authenticated_user(self):
        self.client.login(username="testuser1", password="12345")
        Cart.objects.create(user=self.test_user1, product=self.product, quantity=1)

        response = self.client.post(
            reverse("carts:cart_remove"), {"product_id": self.product.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cart.objects.count(), 0)
