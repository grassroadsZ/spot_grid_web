from django.db import models

# Create your models here.


class SpotConfigModel(models.Model):
    id = models.AutoField(primary_key=True, help_text="自增id")
    next_buy_price = models.DecimalField(decimal_places=8, max_digits=16, help_text="下次开仓价(你下一仓位买入价)",
                                         verbose_name="下次开仓价")
    grid_sell_price = models.DecimalField(decimal_places=8, max_digits=16, help_text="当前止盈价(你的当前仓位卖出价)",
                                          verbose_name="当前止盈价")
    step = models.IntegerField(help_text="当前仓位(0:仓位为空)", verbose_name="当前仓位")
    profit_ratio = models.DecimalField(decimal_places=3, max_digits=4,
                                       help_text="止盈比率(卖出价调整比率。如：设置为5,即为5%，当前买入价为100，那么下次卖出价为105)", verbose_name="止盈比率")
    double_throw_ratio = models.DecimalField(decimal_places=3, max_digits=4,
                                             help_text="补仓比率(买入价调整比率。如：设置为5,即为5%当前买入价为100，那么下次买入价为95)",
                                             verbose_name="补仓比率")
    coin_type = models.CharField(max_length=16, help_text="交易对(你要进行交易的交易对，请参考币安现货。如：BTC 填入 BTCUSDT)",
                                 verbose_name="交易对")
    quantity = models.CharField(max_length=256, help_text="交易数量(第一手买入1,第二手买入2...超过第三手以后的仓位均按照最后一位数量(3)买入),例如:1,2,3",
                                verbose_name="交易数量")
    max_count = models.IntegerField(help_text="连续买入而不卖出的最大次数", verbose_name="连续买入而不卖出的最大次数")
    min_num = models.IntegerField(help_text="交易金额最小位数长度,如0.00001,则填入5", verbose_name="交易金额最小位数长度")
    current_num = models.IntegerField(help_text="当前连续买入次数", verbose_name="当前连续买入次数", default=0)
    current_income = models.DecimalField(decimal_places=6, max_digits=10, help_text="当前收益", verbose_name="当前收益",
                                         default=0)
    if_use = models.BooleanField(verbose_name="是否启用", default=True)
