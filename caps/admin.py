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

class ImageInlineAdmin(admin.TabularInline):
    model = CapsImage
    fields = []
    extra = 0
    max_num = 6

@admin.register(Caps)
class CapsAdmin(admin.ModelAdmin):
    list_display = 'id name price brand is_available'.split()
    list_display_links = ['name']
    list_filter = 'brand size'.split()
    search_fields = 'name brand__name price'.split()
    save_on_top = True
    save_as = True
    list_editable = ["is_available"]
    inlines = [ImageInlineAdmin]
    
    fieldsets = (
        ("Главная информация", {
            "fields": (("brand", "name","price"), "new_price")
        }),
        ("Описание и размер", {
            "fields": (("description", "size"),)
        }),
        ("Чекбоксы", {
            "fields": (("is_available",), 'in_baner') 
        }),
        
    )
    