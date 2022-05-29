from django.contrib import admin
from orders.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['item', 'status', 'price']
    list_display_links = ['item']
    list_editable = ['price', 'status']