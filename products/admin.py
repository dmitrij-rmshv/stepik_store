from django.contrib import admin

from products.models import Basket, Product, ProductCategory

# admin.site.register(Product)
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('on_sale', 'name', 'price', 'quantity', 'category',)
    list_display_links = ('name',)
    fields = (
        ('name', 'category'), 'description', ('price', 'quantity'), 'stripe_product_price_id', ('image', 'on_sale'),
    )
    # readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('-name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp',)
    readonly_fields = ('created_timestamp',)
    extra = 0
