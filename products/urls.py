from django.urls import path

from products.views import (ProductDetailView, ProductsListView, basket_add,
                            basket_edit, basket_remove)

# from django.views.decorators.cache import cache_page


app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    # path('', cache_page(30)(ProductsListView.as_view()), name='index'),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('basket_edit/<int:id>/<int:quantity>/', basket_edit, name='basket_edit'),
]
