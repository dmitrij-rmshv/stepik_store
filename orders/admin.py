from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    fields = (
        ('id', 'created'),
        ('first_name', 'second_name'),
        'email', 'address',
        'basket_history',
        ('status', 'customer')
    )
    readonly_fields = ('id', 'created')
