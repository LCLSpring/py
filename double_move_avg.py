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

# 新建一个数据表，命名为strategy（策略）
# 序号保持和原始数据一致
strategy = pd.DataFrame(index=df.index)

# 添加一个signal字段，用来存储交易信号
strategy['交易信号'] = 0

# 将5日均价保存到avg_5这个字段
strategy['5日均线'] = df['收盘'].rolling(5).mean()

# 同样，将10日均价保存到avg_10
strategy['10日均线'] = df['收盘'].rolling(10).mean()

# 当5日均价大于10日均价时，标记为1；反之标记为0
strategy['交易信号'] = np.where(strategy['5日均线'] > strategy['10日均线'], 1, 0)

# 根据交易信号的变化下单，当交易信号从0变成1时买入，当交易信号从1变成0时卖出
# 交易信号不变时不下单
strategy['下单'] = strategy['交易信号'].diff()

# 这次我们还是给小瓦20万元的启动资金
initial_cash = 200000

# 新建一个数据表positions，序号和strategy数据表保持一致
# 用0替换空值
positions = pd.DataFrame(index=strategy.index).fillna(0)

# 因为A股买卖都是最低100股
# 因此设置stock字段为交易信号的100倍
positions['stock'] = strategy['交易信号'] * 100

# 创建投资组合数据表，用持仓的股票数量乘以股价得出持仓的股票市值
portfolio = pd.DataFrame()
portfolio['stock value'] = positions.multiply(df['收盘'], axis=0)

# 同样仓位的变化就是下单的数量
order = positions.diff()

# 用初始资金减去下单金额的总和就是剩余的资金
portfolio['cash'] = initial_cash - order.multiply(df['收盘'], axis=0).cumsum()

# 剩余的资金 + 持仓股票市值即总资产
portfolio['total'] = portfolio['cash'] + portfolio['stock value']

# 创建10×5的画布
plt.figure(figsize=(10, 5))

# 绘制总资产曲线
plt.plot(portfolio['total'], lw=2, label='total')

# 绘制持仓股票市值曲线
plt.plot(portfolio['stock value'], lw=2, ls='--', label='stock value')

# 添加图注
plt.legend()

# 添加网格
plt.grid()

# 显示图像
plt.show()


