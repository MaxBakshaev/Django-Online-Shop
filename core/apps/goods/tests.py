from django.test import TestCase

from users.models import User
from goods.utils import q_search
from goods.models import Categories, Products, Review


class TestGoods(TestCase):

    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='12345')
        self.test_user1.save()
        Categories.objects.create(name="Книги", slug="knigi", id=1)
        Categories.objects.create(name="Test Category", slug="test-category", id=3)
        Categories.objects.create(name="Автомобили", slug="avtomobili", id=2)
        self.product1 = Products.objects.create(
            name="Лимузин",
            slug="limuzin",
            price=100,
            discount=10,
            quantity=1,
            category_id=2,
            id=1,
        )
        self.product2 = Products.objects.create(
            name="Tesla Cybertruck",
            slug="tesla-cybertruck",
            price=100000,
            discount=0,
            quantity=2,
            category_id=2,
            id=2,
        )
        self.review = Review.objects.create(
            product=self.product1,
            user=self.test_user1,
            rating=4,
            comment='Хороший продукт',
        )
        
    def test_search_by_name(self):
        response = self.client.get("/catalog/search/?q=Лимузин/", {"q": "Лимузин"})
        self.assertEqual(len(response.context["goods"]), 1)
        self.assertEqual(response.context["goods"][0][0], self.product1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goods/catalog.html")

    def test_search_by_id(self):
        response = self.client.get("/catalog/search/?q=2/", {"q": "2"})
        self.assertEqual(len(response.context["goods"]), 1)
        self.assertEqual(response.context["goods"][0][0], self.product2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goods/catalog.html")

    def test_search_no_results(self):
        response = self.client.get("/catalog/search/?q=product/", {"q": "product"})
        self.assertEqual(len(response.context["goods"]), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goods/catalog.html")

    def test_q_search_by_id(self):
        result = q_search("1")
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), self.product1)

    def test_q_search_by_name(self):
        result = q_search("Лимузин")
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), self.product1)

    def test_q_search_no_results(self):
        result = q_search("xbbgsffgbgbf")
        self.assertEqual(result.count(), 0)

    def test_category(self):
        response = self.client.get("/catalog/knigi/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goods/catalog.html")

    def test_product(self):
        response = self.client.get("/catalog/product/limuzin/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goods/product.html")

    def test_get_queryset_all_products(self):
        response = self.client.get(
            "/catalog/avtomobili/", kwargs={"category_slug": "avtomobili"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Лимузин")
        self.assertContains(response, "Tesla Cybertruck")
        self.assertTemplateUsed(response, "goods/catalog.html")

    def test_filter_on_sale(self):
        response = self.client.get(
            "/catalog/avtomobili/?on_sale=on/",
            kwargs={"category_slug": "avtomobili", "on_sale": "on"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Лимузин")
        self.assertNotContains(response, "Tesla Cybertruck")
        self.assertTemplateUsed(response, "goods/catalog.html")

    def test_filter_by_price(self):
        response = self.client.get(
            "/catalog/avtomobili/?order_by=default&cost_1k=on/",
            kwargs={"category_slug": "avtomobili", "cost_1k": "true"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Лимузин")
        self.assertNotContains(response, "Tesla Cybertruck")
        self.assertTemplateUsed(response, "goods/catalog.html")

    def test_pagination(self):
        for i in range(10):
            Products.objects.create(
                name=f"Product {i+1}",
                slug=f"product{i+1}",
                price=100,
                discount=10,
                quantity=1,
                category_id=3,
                id=3+i,
            )
        response = self.client.get(
            '/catalog/test-category/', kwargs={'category_slug': 'Test Category'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Product 1")
        self.assertContains(response, "Product 6")
        self.assertNotContains(response, "Product 7")
        self.assertTemplateUsed(response, "goods/catalog.html")

    def test_goods_amount(self):
        response = self.client.get(
            '/catalog/avtomobili/', kwargs={'category_slug': 'avtomobili'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goods/catalog.html")
        self.assertIn('amount', response.context)
        self.assertEqual(response.context['amount'], 2)

    def test_goods_ending(self):
        Products.objects.create(
            name="test product",
            slug="test-product",
            price=100,
            discount=10,
            quantity=1,
            category_id=3,
            id=3,
        )
        
        response = self.client.get(
            '/catalog/avtomobili/', kwargs={'category_slug': 'avtomobili'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goods/catalog.html")
        self.assertIn('goods_ending', response.context)
        self.assertEqual(response.context['goods_ending'], 'товара')

        response2 = self.client.get(
            '/catalog/knigi/', kwargs={'category_slug': 'knigi'}
        )
        self.assertEqual(response2.context['goods_ending'], 'товаров')
        
        response3 = self.client.get(
            '/catalog/test-category/', kwargs={'category_slug': 'Test Category'}
        )
        self.assertEqual(response3.context['goods_ending'], 'товар')
        
    def test_goods_name(self):
        response = self.client.get(
            '/catalog/avtomobili/', kwargs={'category_slug': 'avtomobili'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['goods'][0][0].name, 'Лимузин')
        
    def test_goods_rating(self):
        response = self.client.get(
            '/catalog/avtomobili/', kwargs={'category_slug': 'avtomobili'})
        self.assertEqual(response.status_code, 200)    
        self.assertEqual(response.context['goods'][0][1][0], 4)
        
    def test_goods_amount_reviews(self):
        response = self.client.get(
            '/catalog/avtomobili/', kwargs={'category_slug': 'avtomobili'})
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.context['goods'][0][1][1], '1 отзыв')
        self.assertEqual(response.context['goods'][0][1][2], 1)
        
        self.assertEqual(response.context['goods'][1][1][1], '0 отзывов')
        self.assertEqual(response.context['goods'][1][1][2], 0)
        
    def test_create_review(self):
        review = Review.objects.create(
            product=self.product2,
            user=self.test_user1,
            rating=5,
            comment='Отличный продукт',
        )
        self.assertIn(review, self.product2.reviews.all())
        self.assertEqual(self.product2.reviews.count(), 1)
        self.assertEqual(review.product, self.product2)
        self.assertEqual(review.user, self.test_user1)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Отличный продукт')
        self.assertIsNotNone(review.created)
