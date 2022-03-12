from django.contrib import admin
from . models import *

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = 'id name'.split()
    list_display_links = ('name',)
    prepopulated_fields = {"slug": ('name',)}
    

@admin.register(Sizes)
class SizesAdmin(admin.ModelAdmin):
    list_display = 'id value'.split()
    list_display_links = ('value',)
    
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass



@admin.register(Caps)
class CapsAdmin(admin.ModelAdmin):
    list_display = 'id name price brand is_available'.split()
    list_display_links = ['name']
    list_filter = 'brand size'.split()
    search_fields = 'name brand__name price'.split()
    save_on_top = True
    save_as = True
    list_editable = ["is_available"]
    
    fieldsets = (
        ("Главная информация", {
            "fields": (("brand", "name","price"), "new_price")
        }),
        ("Описание и размер", {
            "fields": (("description", "size"),)
        }),
        ("Чекбоксы", {
            "fields": (("is_available",),) 
        }),
        
    )
    

@admin.register(UserCapsFavorite)
class FavBasAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_favorite']
    list_editable = ['is_favorite']
    # list_display_links = ['']

@admin.register(CapsImage)
class CapsImageAdmin(admin.ModelAdmin):
    list_display = ['caps']
    list_display_links = ['caps']