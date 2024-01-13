from django.urls import path

from orders.views import (CancelTemplateView, OrderCreateView, OrderDetailView,
                          OrdersListView, SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('', OrdersListView.as_view(), name='orders_list'),
    path('detail/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('success/', SuccessTemplateView.as_view(), name='order_success'),
    path('canceled/', CancelTemplateView.as_view(), name='order_canceled'),
]
