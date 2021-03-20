默认运行环境是国外的服务器,默认环境是python(linux自带的是python2)
首次运行
```shell script
pip install -r requirt.txt 

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser

```
修改spot_grid_web.settings.py 中的 BINANCE_CONFIG 中的对应的key 和secret

python3 manage.py createsuperuser 用于创建后台登录用户
spot_grid_web.wsgi.py 中的    
```scheduler.add_job(spot.spot_start_run, "interval", seconds=30, id="spot_grid_run", replace_existing=True)```
seconds 字段控制间隔时间,每30s会执行一次,如果是1分钟,请设置60

启动运行服务
```shell script
python3 manage.py runserver 
```
运行此命令的窗口请勿关闭

浏览器访问 127.0.0.1:8000/admin
添加币对相关信息在spot_trade 部分

推荐使用在有图形界面的云服务器上运行
# linux运行

需要将```spot_grid_web.settings.py中的ALLOWED_HOSTS = []``` 修改为```ALLOWED_HOSTS = ["*"]```
云服务需要将安全组端口8000 端口开放访问

```shell script
# linux后台 运行命令
nohup python3 manage.py runserver &
```


```markdown
next_buy_price:  币对的买入价格
grid_sell_price:    币对的卖出价格
step: 初始仓位,整数
profit_ratio:   差价盈利率,0.5 代表 0.5%
double_throw_ratio:   差价补仓率 0.5 代表 0.5%
coin_type: 交易对,如BTCUSDT
quantity: 每次买入数量,请填写多个,需要每次买入的数量相同的话也请填写(英文逗号分隔)  如: 1,1
max_count: 连续买入而不卖出的最大次数,用于风控, 整数
current_num：当前连续买入次数，用于风控,整数,当current_num 次数与max_count次数相同时，该币对会自动跳过不买入
current_income:当前收益
if_use: 是否启用,
```
# 需要对已经在运行中的币对进行修改时,需要先将币对状态设置为禁用后保存,然后再对需要修改的币对进行参数修改,添加删除币对不需要先启用禁用

此版交易逻辑代码大部分使用是基于此项目的web版简单实现。

币圈投资需谨慎。。。

[网格交易](https://github.com/hengxuZ/binance-quantization.git)