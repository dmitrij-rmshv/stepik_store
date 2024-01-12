from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_view(self):
        path = reverse('products:index')
        response = self.client.get(path)

        products = [prod for prod in self.products if prod.on_sale][:3]
        self._common_tests(response)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertEqual(list(response.context_data['object_list']), products)

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)
        self._common_tests(response)
        self.assertEqual(response.context_data['title'], 'Каталог - Одежда')
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id).filter(on_sale=True))[:3]
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
