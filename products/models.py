from django.db import models

from users.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категория'
        ordering = ('id',)

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):

    def get_ctg_set(self):
        return set(product.category_id for product in Product.objects.filter(on_sale=True))


class Product(models.Model):
    name = models.CharField(verbose_name='наименование', max_length=256)
    description = models.TextField(verbose_name='описание', )
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='кол.', default=0)
    image = models.ImageField(verbose_name='изображение', upload_to='products_images')
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


class BasketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


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
