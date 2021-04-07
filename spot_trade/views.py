import time

from django import views
from django.db import transaction

from Public_API.binanceAPI import BinanceAPI
from Utils.Ding_Ding import send_dingding_msg

from Utils.help_func import help_print
from spot_grid_web.settings import BINANCE_CONFIG
from spot_trade.models import SpotConfigModel, OrderDetailModels

binance_instance = BinanceAPI(BINANCE_CONFIG.get("api_key"), BINANCE_CONFIG.get("api_secret"))

# 手续费
charge_amount = 0.00075


class SpotTradeView(views.View):


    def update_data(self, coin_info_obj, deal_price, step, current_num):
        # 显式的开启一个事务
        with transaction.atomic():
        # 创建事务保存点
            save_id = transaction.savepoint()
            coin_info_obj.next_buy_price = round(deal_price * (1 - coin_info_obj.double_throw_ratio / 100),
                                                 coin_info_obj.min_num)
            coin_info_obj.grid_sell_price = round(deal_price * (1 + coin_info_obj.profit_ratio / 100),
                                                  coin_info_obj.min_num)
            coin_info_obj.step += step
            coin_info_obj.current_num += current_num
            coin_info_obj.current_num = max([0, coin_info_obj.current_num])
            coin_info_obj.save()
            transaction.savepoint_commit(save_id)


    def loop_run(self):
        for coin_info in SpotConfigModel.objects.filter(if_use=1):
            try:
                cur_market_price = binance_instance.get_ticker_price(coin_info.coin_type)  # 当前交易对市价
                buy_price = coin_info.next_buy_price  # 当前网格买入价格
                sell_price = coin_info.grid_sell_price  # 当前网格卖出价格

                step = coin_info.step  # 当前步数
                current_num = coin_info.current_num  # 当前连续买入次数
                max_count = coin_info.max_no_sell_count  # 连续买入而不卖出的最大次数
                buy_with_no_sell_count_ratio = coin_info.buy_with_no_sell_count_ratio  # 连续买入/最大买入而不卖出的比例
                quantity = coin_info.quantity  # 买入数量
                max_no_buy_count = coin_info.max_no_buy_count  # 连续当前价格大于期望买入价格次数的设置值∂
                max_no_buy_num = coin_info.max_no_buy_num  # 连续当前价格大于期望买入价格次数的设置值∂
                print(
                    "当前交易对:" + coin_info.coin_type + str(list([i for i in coin_info])))

                # 设置的买入价 > 当前现货价格
                if buy_price >= cur_market_price:
                    # 如果当前次数/最大次数大于设置的比例时，取最小的交易量,当前买入次数为0 时也买最少
                    if float(current_num / max_count) > buy_with_no_sell_count_ratio / 10 or step == 0:
                        help_print(
                            "当前交易对:" + coin_info.coin_type + "连续买入次数已达" + str(current_num) + "次,调整为最低购买量" + str(
                                quantity))

                        quantity = quantity

                    else:
                        quantity *= 2  # 买入量

                    if current_num == max_count:
                        help_print("当前交易对:" + coin_info.coin_type + "连续买入次数已达" + str(current_num) + "次,暂停买入")
                        return

                    res = binance_instance.buy_limit_msg(coin_info.coin_type, quantity, buy_price)

                    if res.get('orderId'):  # 挂单成功
                        OrderDetailModels.objects.create(coin_type=coin_info.coin_type, buy_sell="buy", price=buy_price)
                        self.update_data(coin_info, buy_price, 1, 1)  # 修改买入卖出价格、当前步数
                elif sell_price < cur_market_price:  # 是否满足卖出价
                    if step == 0:  # setp=0 防止踏空，跟随价格上涨
                        self.update_data(coin_info, sell_price, step, 0)
                    else:
                        quantity = quantity if step < 2 else quantity * 2
                        res = binance_instance.sell_limit_msg(coin_info.coin_type, quantity, sell_price)
                        if res.get('orderId'):
                            # coin_info.current_income = (1 - charge_amount) * sell_price * quantity - (
                            #         1 + charge_amount) * buy_price * quantity
                            OrderDetailModels.objects.create(coin_type=coin_info.coin_type, buy_sell="sell",
                                                             price=buy_price)
                            self.update_data(coin_info, sell_price, - 1, -1)

                # 现价 > 期望买入价格 且现价 > 期望卖出价格 且 这个次数 > 设定值，就以现价买入
                if step > 0:
                    if buy_price < cur_market_price:
                        # 计数+1
                        coin_info.max_no_buy_num += 1
                        coin_info.save()

                        if max_no_buy_count > max_no_buy_num:
                            res = binance_instance.buy_limit_msg(coin_info.coin_type, quantity, cur_market_price)

                            if res.get('orderId'):  # 挂单成功
                                OrderDetailModels.objects.create(coin_type=coin_info.coin_type, buy_sell="buy",
                                                                 price=cur_market_price)

                                self.update_data(coin_info, buy_price, 1, 1)  # 修改买入卖出价格、当前步数

            # transaction.savepoint_commit(save_id)

            except Exception as e:
                print(f"{coin_info.coin_type} 币种运行失败,原因为:{e}")
