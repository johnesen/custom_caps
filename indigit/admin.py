from django.contrib import admin

from indigit.models import CapsInDigit

@admin.register(CapsInDigit)
class IndigitAdmin(admin.ModelAdmin):
    list_display = 'id saled year_in_market clients'.split()
    list_display_links = 'saled year_in_market clients'.split()
    
