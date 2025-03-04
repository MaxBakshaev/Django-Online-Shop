from typing import Any, Literal


class GoodsMixin:
    
    def get_product_rating(self) -> Any | Literal[0]:
        """ Возвращает оценку продукта """
        rate = 0
        for review in self.reviews:
            rate += review.rating
        try:
            product_rating = rate / self.amount_reviews
        except ZeroDivisionError:
            product_rating = 0
        return product_rating
    
    def get_reviews_ending(self) -> Literal['отзыв'] | Literal['отзыва'] | Literal['отзывов']:
        """Возвращает слово 'отзыв' в правильном падеже"""
        last_number_of_amount: str = (str(self.amount_reviews))[len(str(self.amount_reviews)) - 1]
        if last_number_of_amount == "1" and str(self.amount_reviews) != "11":
            reviews_ending = "отзыв"
        elif last_number_of_amount in ["2", "3", "4"] and str(self.amount_reviews) not in ["12", "13", "14"]:
            reviews_ending = "отзыва"
        else:
            reviews_ending = "отзывов"
        return reviews_ending
    
    def get_goods_ending(self) -> Literal["товар"] | Literal["товара"] | Literal["товаров"]:
        """Возвращает слово 'товар' в правильном падеже"""
        last_number_of_amount: str = (str(self.amount))[len(str(self.amount)) - 1]
        if last_number_of_amount == "1" and str(self.amount) != "11":
            goods_ending = "товар"
        elif last_number_of_amount in ["2", "3", "4"] and str(self.amount) not in ["12","13","14",]:
            goods_ending = "товара"
        else:
            goods_ending = "товаров"
        return goods_ending
    
    def get_products_list(self) -> list[tuple]:
        """ 
        Возвращает список товаров, где элементы:
        Первый кортеж - продукт (объект из queryset)
        Второй кортеж - оценка и количество отзывов о продукте
        """

        # список оценок продуктов
        goods_rating_list = []
        # список количества отзывов продуктов
        goods_amount_reviews_list = []

        for product in self.goods:

            # получение количества отзывов о продуктах и слово "отзыв" в правильном падеже
            self.reviews = product.reviews.all()
            self.amount_reviews: int = len(self.reviews)
            reviews_ending = self.get_reviews_ending()
            goods_amount_reviews_list.append(f"{self.amount_reviews} {reviews_ending}")

            # получение оценки продуктов
            rating = self.get_product_rating()
            goods_rating_list.append(rating)

        dict_product_rating_amount_reviews = {}
        product_index = 0
        for good in self.goods:
            dict_product_rating_amount_reviews[self.goods[product_index]] = (
                goods_rating_list[product_index],
                goods_amount_reviews_list[product_index],
            )
            product_index += 1
        return list(dict_product_rating_amount_reviews.items())
