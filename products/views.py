from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView

from products.models import Basket, Product, ProductCategory


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    new_prod_number = 9
    try:
        novelties = ProductCategory.objects.get(name='Новинки').id
    except ObjectDoesNotExist:
        novelties = None

    def get_paginate_by(self, queryset):
        if self.kwargs.get('category_id'):
            return self.paginate_by * 2
        else:
            return self.paginate_by

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset().filter(on_sale=True)
        category_id = self.kwargs.get('category_id')
        if category_id:
            return queryset.filter(category_id=category_id) if category_id else queryset
        return queryset.order_by('-id')[:self.new_prod_number]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        category_id = self.kwargs.get('category_id')
        title = f'Каталог - {ProductCategory.objects.get(id=category_id).name}' if category_id else 'Store - Каталог'
        present_categories = Product.objects.get_ctg_set()
        if self.novelties:
            present_categories.add(self.novelties)
        context['title'] = title
        context['categories'] = ProductCategory.objects.all()
        context['present_categories'] = present_categories
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        title = f'Купить {Product.objects.get(id=self.kwargs["pk"]).name}'
        context['title'] = title
        back_url = self.request.META['HTTP_REFERER']
        context['back_url'] = back_url
        return context


@login_required
def basket_add(request, product_id):
    Basket.create_or_update(product_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # return HttpResponseRedirect(request.path)


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket = Basket.objects.get(id=int(id))
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets': baskets}
        result = render_to_string('products/baskets.html', context)
    return JsonResponse({'result': result})
