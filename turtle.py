import akshare as ak
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

# 推荐字体路径（macOS）
font_path = "/System/Library/Fonts/PingFang.ttc"
font_prop = fm.FontProperties(fname=font_path)

# 设置 matplotlib 使用它
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# 比亚迪 A 股的股票代码：002594（深市）
stock_code = "002594"

# 获取历史行情数据
df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date="20250101", end_date="20250630", adjust="qfq")
df = df[["日期", "收盘", "涨跌额"]]

# 创建一个名为turtle的数据表，使用原始数据表的日期序号
turtle = pd.DataFrame(index = df.index)

# 设置唐奇安通道的上沿为前5天股价的最高点
turtle['high'] = df['收盘'].shift(1).rolling(5).max()

# 设置唐奇安通道的下沿为过去5天的最低点
turtle['low'] = df['收盘'].shift(1).rolling(5).min()

# 当股价突破上沿时，发出买入信号
turtle['buy'] = df['收盘'] > turtle['high']

# 当股价跌破下沿时，发出卖出信号
turtle['sell'] = df['收盘'] < turtle['low']

# 初始的订单状态为0
turtle['orders'] = 0

# 初始的仓位为0
position = 0

# 设置循环，遍历turtle数据表
for k in range(len(turtle)):
    # 当买入信号为True且仓位为0时下单买入1手
    if turtle.buy[k] and position == 0:
        # 修改对应的orders值为1
        turtle.orders.values[k] = 1
        # 仓位也增加1手
        position = 1
    # 当卖出信号为True且有持仓时卖出1手
    elif turtle.sell[k] and position > 0:
        # orders的值修改为-1
        turtle.orders.values[k] = -1
        # 仓位相应清零
        position = 0

# 再次给小瓦2万元初始资金
initial_cash = 200000

# 创建新的数据表，序号和turtle数据表一致
positions = pd.DataFrame(index=turtle.index).fillna(0.0)

# 每次交易为1手，即100股，仓位即买单和卖单的累积加和
positions['stock'] = 100 * turtle['orders'].cumsum()

# 创建投资组合数据表
portfolio = positions.multiply(df['收盘'], axis=0)

# 持仓市值为持仓股票数量乘以股价
portfolio['holding_values'] = (positions.multiply(df['收盘'], axis=0))

# 计算出仓位的变化
pos_diff = positions.diff()

# 剩余的现金是初始资金减去仓位变化产生的现金流累计算和
portfolio['cash'] = initial_cash - (pos_diff.multiply(df['收盘'], axis=0)).cumsum()

# 总资产即持仓股票市值加剩余现金
portfolio['total'] = portfolio['cash'] + portfolio['holding_values']

# 使用可视化的方式展示
plt.figure(figsize=(10,5))
plt.plot(portfolio['total'])
plt.plot(portfolio['holding_values'], '--')
plt.grid()
plt.legend()
plt.show()

print(portfolio.tail(20))

