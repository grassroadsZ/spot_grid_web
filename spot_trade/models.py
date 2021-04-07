from django.db import models


# Create your models here.


class SpotConfigModel(models.Model):
    class Meta:
        db_table = "td_grid_config"

    verbose_name = '无限网格策略表'
    verbose_name_plural = verbose_name

    id = models.AutoField(primary_key=True, help_text="自增id")
    next_buy_price = models.DecimalField(decimal_places=8, max_digits=16, help_text="下次买入(你下一仓位买入价)",
                                         verbose_name="下次买入价")
    grid_sell_price = models.DecimalField(decimal_places=8, max_digits=16, help_text="当前止盈价(你的当前仓位卖出价)",
                                          verbose_name="当前止盈价")
    step = models.IntegerField(help_text="当前已经买入几次", verbose_name="当前已经买入几次")
    profit_ratio = models.DecimalField(decimal_places=3, max_digits=4,
                                       help_text="止盈比率(卖出价调整比率。如：设置为5,即为5%，当前买入价为100，那么下次卖出价为105)", verbose_name="止盈比率")
    double_throw_ratio = models.DecimalField(decimal_places=3, max_digits=4,
                                             help_text="补仓比率(买入价调整比率。如：设置为5,即为5%当前买入价为100，那么下次买入价为95)",
                                             verbose_name="补仓比率")
    coin_type = models.CharField(max_length=16, help_text="交易对(你要进行交易的交易对，请参考币安现货。如：BTC 填入 BTCUSDT)",
                                 verbose_name="交易对")
    quantity = models.CharField(max_length=256, help_text="买入数量",
                                verbose_name="交易数量")
    max_no_sell_count = models.IntegerField(help_text="连续买入而不卖出的最大次数", verbose_name="连续买入而不卖出的最大次数")
    buy_with_no_sell_count_ratio = models.SmallIntegerField(verbose_name="连续买入/最大买入而不卖出的比例,设置为1则是 连续买入/最大买入而不卖出 = 0.1 ",
                                                            default=4)
    max_no_buy_count = models.SmallIntegerField(help_text="连续当前价格大于期望买入价格次数设置值", verbose_name="连续当前价格大于期望买入价格设置值",default=0)
    max_no_buy_num = models.SmallIntegerField(help_text="连续当前价格大于期望买入价格计数", verbose_name="连续当前价格大于期望买入计数",default=0)

    min_num = models.IntegerField(help_text="交易金额最小位数长度,如0.00001,则填入5", verbose_name="交易金额最小位数长度")
    current_num = models.IntegerField(help_text="当前连续买入次数", verbose_name="当前连续买入次数", default=0)
    if_use = models.BooleanField(verbose_name="是否启用", default=True)


class OrderDetailModels(models.Model):
    class Meta:
        db_table = "td_order_detail"
        verbose_name = '订单记录'
        verbose_name_plural = verbose_name

    coin_type = models.CharField(verbose_name="交易币对", help_text="交易币对", max_length=12)
    strategy_name = models.CharField(verbose_name="使用的自定义策略名称", help_text="使用的自定义策略名称", max_length=64, default="grid")
    buy_sell = models.CharField(default=None, verbose_name="买卖方向", max_length=6)
    price = models.DecimalField(max_digits=16, decimal_places=4, verbose_name="单价")
    time = models.DateTimeField(auto_now=True, verbose_name="交易时间")
    status = models.BooleanField(default=False, verbose_name="是否以汇总")
