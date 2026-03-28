from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem

admin.site.site_header = "ShopZone Admin"
admin.site.site_title = "ShopZone"
admin.site.index_title = "Store Management"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'rating', 'is_featured']
    list_filter = ['category', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_featured']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'total_price', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method']
    inlines = [OrderItemInline]
    readonly_fields = ['user', 'total_price', 'created_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'total_items', 'total_price']
