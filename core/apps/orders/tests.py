from django.test import TestCase
from django.urls import reverse

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
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

    def test_redirect_if_user_not_logged(self):

        response1 = self.client.get("/orders/create-order/")
        self.assertEqual(response1.status_code, 302)
        self.assertRedirects(response1, "/user/login/?next=/orders/create-order/")

        response2 = self.client.get("/orders/my-orders/")
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, "/user/login/?next=/orders/my-orders/")

    def test_user_is_logged(self):

        self.client.login(username="testuser1", password="12345")

        response1 = self.client.get("/orders/create-order/")
        self.assertEqual(response1.status_code, 200)
        self.assertTemplateUsed(response1, "orders/create_order.html")

        response2 = self.client.get("/orders/my-orders/")
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, "orders/my_orders.html")

    def test_create_order(self):
        self.client.login(username="testuser1", password="12345")
        Cart.objects.create(user=self.test_user1, product=self.product, quantity=1)
        response = self.client.post(
            reverse("orders:create_order"),
            {
                "first_name": "Test",
                "last_name": "User",
                "phone_number": "1234567890",
                "requires_delivery": "1",
                "delivery_address": "Test Address",
                "payment_on_get": "0",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cart.objects.count(), 0)
        self.assertTrue(Order.objects.filter(user=self.test_user1).exists())
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_invalid_phone(self):
        self.client.login(username="testuser1", password="12345")
        Cart.objects.create(user=self.test_user1, product=self.product, quantity=1)

        form_data = {
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "invalid_phone",
            "requires_delivery": "1",
            "delivery_address": "Test Address",
            "payment_on_get": "0",
        }
        form = CreateOrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)

    def test_create_order_invalid_name(self):
        self.client.login(username="testuser1", password="12345")
        Cart.objects.create(user=self.test_user1, product=self.product, quantity=1)

        response = self.client.post(
            reverse("orders:create_order"),
            {
                "first_name": "",
                "last_name": "User",
                "phone_number": "1234567890",
                "requires_delivery": "1",
                "delivery_address": "Test Address",
                "payment_on_get": "0",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_item_creation(self):
        self.client.login(username="testuser1", password="12345")
        Cart.objects.create(user=self.test_user1, product=self.product, quantity=10)

        order = Order.objects.create(
            user=self.test_user1,
            phone_number="1234567890",
            requires_delivery=True,
            delivery_address="Test Address",
            payment_on_get=False,
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            name=self.product.name,
            price=self.product.price,
            quantity=10,
        )

        self.assertEqual(OrderItem.objects.count(), 1)
