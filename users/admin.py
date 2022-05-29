from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import User, Basket
from orders.models import Order


# @admin.register(Order)
class OrdersInline(admin.TabularInline):
    model = Order
    fields = ['item', 'status', 'user', 'price', 'send_date']
    extra =   0
    # readonly_fields = ['item']


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'phone', 'is_verified', 'is_active',)
    list_filter = ('is_superuser',)
    list_editable = ('is_verified',)
    readonly_fields = ('date_joined', 'last_login', 'last_active')
    fieldsets = (
        ('Основное', {'fields': ('username', 'email', 'first_name', 'last_name', 'phone', 'password', 'photo', 'favourites')}),
        ('Даты', {'fields': ('date_joined', 'last_login', 'last_active')}),
        ('Разрешения', {'fields': ('is_superuser', 'is_verified', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'photo', 'password1', 'password2', 'is_active',)}
         ),
    )
    search_fields = ('email', 'phone')
    ordering = ('email',)
    list_display_links = ('username', 'email', 'phone',)
    inlines = [OrdersInline]


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)

admin.site.site_header = _("CustomCaps Admin")
admin.site.register(Basket)