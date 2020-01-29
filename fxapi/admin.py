from django.contrib import admin
from .models import Symbol, Option, ComfortZones
from django_admin_listfilter_dropdown.filters import DropdownFilter, ChoiceDropdownFilter

@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = (
        'symbol',
        'fx_symbol',
        'name',
        'point_price',
        'cab',
        'is_enabled',
    )
    ordering = ('symbol', )

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = (
        'symbol',
        'option_type',
        'option_code',
        'expiration',
    )
    ordering = ('symbol', )
    list_filter = (
    	('symbol__symbol', DropdownFilter),
    	'option_type',
    )

@admin.register(ComfortZones)
class ComfortZonesAdmin(admin.ModelAdmin):
    list_display = (
        'symbol',
        'option_code',
        'zone_type',
        'start_date',
        'end_date',
        'call_strike',
        'balance',
        'put_strike',
    )
    ordering = ('symbol', )