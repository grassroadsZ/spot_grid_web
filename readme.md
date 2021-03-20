默认运行环境是国外的服务器,默认环境是python(linux自带的是python2)
首次运行
```shell script
pip install -r requirt.txt 

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser

```
界面上添加需要交易的交易对
[![6hRmgs.png](https://z3.ax1x.com/2021/03/20/6hRmgs.png)](https://imgtu.com/i/6hRmgs)

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

先执行以下命令
```shell script
python3 -m venv venv
source venv/bin/activate
```
然后再执行以下命令
```shell script
pip install -r requirt.txt 

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```

注意linux每次运行前需先在有venv目录的层级执行```source venv/bin/activate```

linux系统运行报如下错误时运行```pip install django==2.1.8``` 然后再次运行即可：
```shell script
    ...
    raise ImproperlyConfigured('SQLite 3.8.3 or later is required (found %s).' % Database.sqlite_version)
django.core.exceptions.ImproperlyConfigured: SQLite 3.8.3 or later is required (found 3.7.17).
```

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

# 主要解决问题
- 提供web页面进行交易对币种的增加/删除/启用,无需停止程序(2分钟左右即可生效)
- 运行一份代码即可跑多个交易对的网格
- 当连续买入而不卖出次数等于最大买入次数时会该币对会停止买入
- 以定时任务的形式每分钟查询设置的交易对进行运行,目前自测设置10个交易对完整运行一次需要23s左右(hk服务器),交易对过多时建议将60s时间间隔设置更大

# 待解决问题
- 不同情况买入数量不同未解决,如设置1,2,3 实际买入只会取1或者3

佛系更新,业余选手

linux 运行提示[端口被占用解决方案](https://blog.csdn.net/whdxjbw/article/details/80681191)

