from django.contrib import admin

# Register your models here.
from .models import SpotConfigModel


class SpotConfigModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'coin_type', 'next_buy_price', 'grid_sell_price', 'step', 'profit_ratio', 'double_throw_ratio',
        'quantity', "min_num",)


    fieldsets = (

        ("交易对", {'fields': (("coin_type",))}),

        ('交易设置', {'fields': (
            ("next_buy_price", "grid_sell_price",), "step", "quantity", ('profit_ratio', 'double_throw_ratio'))}),
        ("风控设置", {'fields': (
            ("max_no_buy_count", "min_num", "max_no_buy_num", "current_num", "buy_with_no_sell_count_ratio","max_no_sell_count"))}),)


admin.site.register(SpotConfigModel, SpotConfigModelAdmin)
