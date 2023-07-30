from django.contrib.auth.decorators import login_required
from django.core.cache import cache
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

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.category_id = self.kwargs.get('category_id', 0)

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset().filter(on_sale=True)
        if self.category_id:
            return queryset.filter(category_id=self.category_id)
        else:
            return queryset.order_by('-id')[:self.new_prod_number]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.category_id:
            title = f'Каталог - {ProductCategory.objects.get(id=self.category_id).name}'
        else:
            title = 'Store - Каталог'
        context['title'] = title
        # categories = cache.get('categories')
        # if categories:
        #     context['categories'] = categories
        # else:
        #     cache.set('categories', ProductCategory.objects.all(), 30)
        #     context['categories'] = cache.get('categories')
        context['categories'] = cache.get_or_set('categories', ProductCategory.objects.all(), 300)
        # context['categories'] = ProductCategory.objects.all()
        context['present_categories'] = Product.objects.get_ctg_set()
        context['current_category'] = self.category_id
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
