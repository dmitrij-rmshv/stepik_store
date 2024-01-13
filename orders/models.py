from django.db import models

from products.models import Basket, Product
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен')
    )

    first_name = models.CharField(verbose_name='имя получателя', max_length=128)
    second_name = models.CharField(verbose_name='фамилия получателя', max_length=128)
    email = models.EmailField(max_length=256)
    address = models.CharField(verbose_name='адрес доставки', max_length=256)
    customer = models.ForeignKey(verbose_name='заказчик', to=User, on_delete=models.CASCADE)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)

    def __str__(self):
        return f'Заказ № {self.id}. Заказчик: {self.first_name} {self.second_name}'

    def update_after_payment(self):
        print('вызов update_after_payment')
        baskets = Basket.objects.filter(user=self.customer)
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum())
        }
        # а теперь бы опустошить склад:
        for basket in baskets:
            new_in_stock = basket.product.quantity - basket.quantity
            basket.product.quantity = new_in_stock
            basket.product.save()
            Product.update_stripe_product_qty(basket.product, new_in_stock)
        # TODO а не плохо бы дополнительно провериться на отсутствие закупаемого количества товара на складе
        baskets.delete()
        self.save()
