import akshare as ak
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm

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
period = 10
avg_10 = []
avg_value = []
for price in df['收盘']:
    avg_10.append(price)
    if len(avg_10) > period:
        del avg_10[0]
    avg_value.append(np.mean(avg_10))
df['10日均价'] = avg_value

# 设置图像尺寸为10×6
plt.figure(figsize=(10,6))
# 绘制股价的变化
plt.plot(df['收盘'], lw=2, c='k', label='价格')
# 绘制10日均线
plt.plot(df['10日均价'], '--', lw=2, c='b', label='10日均价')
# 添加图注和网格
plt.legend()
plt.grid()
# 将图像进行显示
plt.show()