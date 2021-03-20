import time

from django import views

from Public_API.binanceAPI import BinanceAPI

from Utils.help_func import help_print
from spot_grid_web.settings import BINANCE_CONFIG
from spot_trade.models import SpotConfigModel

binance_instance = BinanceAPI(BINANCE_CONFIG.get("api_key"), BINANCE_CONFIG.get("api_secret"))

# 手续费
charge_amount = 0.00075


class SpotTradeView(views.View):

    def get_quantity(self, coin_info_obj, min_quantity=False):
        '''
        :param exchange: min_quantity用于控制减仓
        :return:
        '''

        quantity_arr = coin_info_obj.quantity.split(",")

        if min_quantity:
            quantity = quantity_arr[0]

        else:
            quantity = quantity_arr[-1]

        return float(quantity)

    def update_data(self, coin_info_obj, deal_price, step, current_num):
        coin_info_obj.next_buy_price = round(deal_price * (1 - coin_info_obj.double_throw_ratio / 100),
                                             coin_info_obj.min_num)
        coin_info_obj.grid_sell_price = round(deal_price * (1 + coin_info_obj.profit_ratio / 100),
                                              coin_info_obj.min_num)
        coin_info_obj.step += step
        coin_info_obj.current_num += current_num
        coin_info_obj.current_num = max([0, coin_info_obj.current_num])
        coin_info_obj.save()

    def loop_run(self):
        for coin_info in SpotConfigModel.objects.filter(if_use=1):
            try:
                cur_market_price = binance_instance.get_ticker_price(coin_info.coin_type)  # 当前交易对市价
                buy_price = coin_info.next_buy_price  # 当前网格买入价格
                sell_price = coin_info.grid_sell_price  # 当前网格卖出价格
                quantity = self.get_quantity(coin_info)
                step = coin_info.step  # 当前步数
                current_num = coin_info.current_num  # 当前连续买入次数
                max_count = coin_info.max_count  # 连续买入而不卖出的最大次数
                help_print(coin_info.coin_type + " 当前现价为： " + str(cur_market_price) + "\t期望买入价为：" + str(
                    buy_price) + "\t期望卖出价为：" + str(sell_price) + "\n")
                # 设置的买入价 > 当前现货价格
                if buy_price >= cur_market_price:
                    # 如果当前次数/最大次数大于40%时，取最小的交易量
                    if float(current_num / max_count) > 0.4:
                        quantity = self.get_quantity(coin_info, min_quantity=True)
                        help_print(
                            "当前交易对:" + coin_info.coin_type + "连续买入次数已达" + str(current_num) + "次,调整为最低购买量" + str(
                                quantity))
                    else:
                        quantity = self.get_quantity(coin_info)  # 买入量

                    if current_num == max_count:
                        help_print("当前交易对:" + coin_info.coin_type + "连续买入次数已达" + str(current_num) + "次,暂停买入")
                        return

                    res = binance_instance.buy_limit(coin_info.coin_type, quantity, buy_price)

                    if res.status_code == 200:  # 挂单成功
                        self.update_data(coin_info, buy_price, 1, 1)  # 修改买入卖出价格、当前步数,连续买入的次数
                        time.sleep(1)

                elif sell_price < cur_market_price:  # 是否满足卖出价
                    if step == 0:  # setp=0 防止踏空，跟随价格上涨
                        self.update_data(coin_info, sell_price, step, 0)
                    else:
                        res = binance_instance.sell_limit(coin_info.coin_type, self.get_quantity(coin_info, False),
                                                          sell_price)
                        if res.status_code == 200:
                            money = float((1 - charge_amount)) * float(sell_price) * quantity - float((
                                    1 + charge_amount)) * float(buy_price) * quantity
                            income = coin_info.current_income

                            coin_info.current_income = money + float(income)

                            self.update_data(coin_info, sell_price, - 1, -1)

                            help_print(coin_info.coin_type + "卖出价为：\n" + str(sell_price) + "\n数量为： " + str(
                                quantity) + "\n盈利为： " + str(money) + "\n总盈利为： " + str(coin_info.current_income))

                            coin_info.save()
                            time.sleep(1)
            except Exception as e:
                print(f"{coin_info.coin_type} 币种运行失败,原因为：{e}")
                print(f"{coin_info.coin_type} 币种运行失败")
