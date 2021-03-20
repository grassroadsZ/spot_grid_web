from django.contrib import admin

# Register your models here.
from .models import SpotConfigModel


class SpotConfigModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'coin_type', "if_use", 'next_buy_price', 'grid_sell_price', 'step', 'profit_ratio', 'double_throw_ratio',
        'quantity', "max_count", "min_num", "current_income")

    fieldsets = (

        ("交易对", {'fields': (("coin_type", "if_use"))}),

        ('交易设置', {'fields': (
        ("next_buy_price", "grid_sell_price",), "step", "quantity", ('profit_ratio', 'double_throw_ratio'))}),
        ("风控设置", {'fields': (("max_count", "min_num",))}),)


admin.site.register(SpotConfigModel, SpotConfigModelAdmin)
