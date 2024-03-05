import stripe
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):

    @staticmethod
    def get_ctg_set():
        return set(product.category_id for product in Product.objects.filter(on_sale=True))


class Product(models.Model):
    name = models.CharField(verbose_name='наименование', max_length=256)
    description = models.TextField(verbose_name='описание', )
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='кол.', default=0)
    image = models.ImageField(verbose_name='изображение', upload_to='products_images', null=True, blank=True)
    stripe_product_price_id = models.CharField(verbose_name='stripe_price.id', max_length=64, null=True, blank=True)
    category = models.ForeignKey(verbose_name='категория', to=ProductCategory, on_delete=models.CASCADE)
    on_sale = models.BooleanField(verbose_name='on', default=True)  # ɥҔɧʮЊЋѤҾӔῷ₪√♦♯￼

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return f'{self.name} | категория: {self.category.name}'
        # return f'Продукт: {self.name} | Категория: {self.category.name}'  # author variant

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None,
                                  update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(
            name=self.name,
            active=self.on_sale,
            description=self.description,
            metadata={
                'category': self.category.name,
                'in_stock': self.quantity
            }
        )
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            currency='rub',
            unit_amount=round(self.price * 100)
        )
        return stripe_product_price

    def update_stripe_product_qty(self, new_qty):
        stripe_product_id = stripe.Price.retrieve(self.stripe_product_price_id)['product']
        metadata = stripe.Product.retrieve(stripe_product_id)['metadata']
        metadata['in_stock'] = new_qty
        stripe.Product.modify(
            stripe_product_id,
            metadata=metadata,
        )

    def delete_stripe_product(self):
        pass

    # def fill_prod_id(self):
    #     stripe_product = stripe.Product.search()


class BasketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            line_items.append(
                {
                    'price': basket.product.stripe_product_price_id,
                    'quantity': basket.quantity
                }
            )
        return line_items


class Basket(models.Model):
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'basket item'
        verbose_name_plural = 'basket items'
        ordering = ('id',)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username.upper()} | Продукт: {self.product.name} | {self.quantity} шт.'

    def sum(self):
        return self.quantity * self.product.price

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return basket_item

    @classmethod
    def create_or_update(cls, product_id, user):
        # product = Product.objects.get(id=product_id)
        try:
            basket = Basket.objects.get(user=user, product_id=product_id)
            basket.quantity += 1
            basket.save()
            is_created = False
        except ObjectDoesNotExist:
            basket = Basket.objects.create(user=user, product_id=product_id, quantity=1)
            is_created = True

        return basket, is_created
