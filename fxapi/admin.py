from django.contrib import admin
from .models import Symbol, Option, ComfortZones

@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display 	= ('symbol', 'name', 'is_enabled',)
    search_fields 	= ('symbol', 'name', )
    ordering 		= ('symbol', )

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display 	= ('symbol', 'option_type', 'option_code', 'expiration',)
    search_fields 	= ('symbol', 'option_type', )
    ordering 		= ('symbol', )

@admin.register(ComfortZones)
class ComfortZonesAdmin(admin.ModelAdmin):
    list_display 	= ('option', 'zone_type', 'start_date','end_date','call_settle','put_settle','balance',)
    search_fields 	= ('option', 'zone_type', )
    ordering 		= ('option', )