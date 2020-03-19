import time
import datetime
from django.db import models


class Symbol(models.Model):
    symbol 		= models.CharField(max_length=10)
    fx_symbol	= models.CharField(max_length=10, null=True, blank=True)
    name 		= models.CharField(max_length=255, null=True, blank=True)
    cme_code 	= models.CharField(max_length=255, null=True, blank=True)
    cme_pid 	= models.CharField(max_length=10, null=True, blank=True)
    exchange 	= models.CharField(max_length=255, null=True, blank=True)
    point_price = models.FloatField(null=True)
    cab			= models.FloatField(null=True)
    is_enabled 	= models.BooleanField(default=True)

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name = ('symbol')
        verbose_name_plural = ('symbols')
        db_table = 'symbols'

class Option(models.Model):
	symbol 			= models.ForeignKey(Symbol, on_delete=models.CASCADE)
	option_type		= models.CharField(max_length=255, null=True, blank=True)
	option_code 	= models.CharField(max_length=255, null=True, blank=True)
	expiration		= models.DateField(null=True)

	def __str__(self):
		return self.option_code

	class Meta:
		verbose_name = ('option')
		verbose_name_plural = ('options')
		db_table = 'options'

class ComfortZones(models.Model):
	symbol 			= models.ForeignKey(Symbol, on_delete=models.CASCADE, default=None)
	fx_symbol		= models.CharField(max_length=10, null=True, blank=True)
	option_code 	= models.CharField(max_length=255, null=True, blank=True)
	zone_type		= models.CharField(max_length=255, null=True, blank=True)
	start_date		= models.DateField(null=True)
	end_date		= models.DateField(null=True)
	call_strike		= models.FloatField(null=True)
	put_strike		= models.FloatField(null=True)
	balance			= models.FloatField(null=True)

	def __str__(self):
		return self.option_code

	class Meta:
		verbose_name = ('comfort_zone')
		verbose_name_plural = ('comfort_zones')
		db_table = 'comfort_zones'

class ComfortZonesCreateResult(models.Model):
	result = models.CharField(max_length=255, null=True, blank=True)

	def __str__(self):
		return self.result

	class Meta:
		verbose_name = ('comfort_zone_create_result')
		verbose_name_plural = ('comfort_zone_create_results')
		db_table = 'comfort_zone_create_results'