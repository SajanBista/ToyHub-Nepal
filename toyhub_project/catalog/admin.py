"""
from django.contrib import admin
from .models import Product, Category, Order, OrderItem

admin.site.register(Product)
admin.site.register(Category)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user', 
        'created_at', 
        'address',
        'ordered_items_summary', 
        'get_total_price',
    )
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'id', 'address')
    inlines = [OrderItemInline]

    def get_total_price(self, obj):
        return obj.total_price()
    get_total_price.short_description = 'Total Price'

    def ordered_items_summary(self, obj):
        return ", ".join(
            f"{item.product.name} (x{item.quantity})" for item in obj.orderitem_set.all()
        )
    ordered_items_summary.short_description = 'Products & Quantity'

admin.site.register(Order, OrderAdmin)
"""
from django.contrib import admin
from .models import Product, Category, OrderItem, Order

# Registering Product and Category with default admin
admin.site.register(Category)

# Inline for OrderItem within OrderAdmin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price', 'total_amount_display')
    readonly_fields = ('total_amount_display',)

    def total_amount_display(self, obj):
        return f"Rs. {obj.total_amount():,.2f}"
    total_amount_display.short_description = 'Total'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'address', 'status', 'ordered_items_summary', 'get_total_price')
    list_filter = ('created_at', 'user', 'status')
    search_fields = ('user__username', 'id', 'address')
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('orderitem_set__product')

    def get_total_price(self, obj):
        return f"Rs. {obj.total_price():,.2f}"
    get_total_price.short_description = 'Total Price'

    def ordered_items_summary(self, obj):
        return ", ".join(
            f"{item.product.name} (x{item.quantity})" for item in obj.orderitem_set.all()
        )
    ordered_items_summary.short_description = 'Products & Quantity'



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total_amount_display')
    search_fields = ('order__id', 'product__name')

    def total_amount_display(self, obj):
        return f"Rs. {obj.total_amount():,.2f}"
    total_amount_display.short_description = 'Total'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock']
    search_fields = ['name']

admin.site.register(Product, ProductAdmin)
