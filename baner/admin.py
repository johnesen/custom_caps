from django.contrib import admin

from baner.models import Baner

@admin.register(Baner)
class BanerAdmin(admin.ModelAdmin):
    list_display = 'id baner_title baner'.split()
    list_display_links = ['baner_title']
