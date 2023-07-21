from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView, TemplateView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    new_prod_number = 9
    try:
        novelties = ProductCategory.objects.get(name='Новинки').id
    except ObjectDoesNotExist:
        novelties = None
        # novelties = tuple()
    # novelties = ProductCategory.objects.get(name='Новинки').id
    # novelties = 5

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset().filter(on_sale=True)
        category_id = self.kwargs.get('category_id')
        if category_id and category_id == self.novelties:
        # if category_id == self.novelties:
            return queryset.order_by('-id')[:self.new_prod_number]
        return queryset.filter(category_id=category_id) if category_id else queryset

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


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        basket = Basket.objects.get(user=request.user, product=product)
        basket.quantity += 1
        basket.save()
    except ObjectDoesNotExist:
        Basket.objects.create(product=product, user=request.user, quantity=1)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # return HttpResponseRedirect(request.path)


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
