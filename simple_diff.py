import akshare as ak
import numpy as np
import matplotlib.pyplot as plt

# 比亚迪 A 股的股票代码：002594（深市）
stock_code = "002594"

# 获取历史行情数据
df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date="20250601", end_date="20250630", adjust="qfq")

df["交易信号"] = np.where(df["涨跌额"] >0, 1, 0)

# 设置画布的尺寸为10*5
plt.figure(figsize=(10, 5))

# 使用折线图绘制出每天的收盘价
df['收盘'].plot(linewidth=2, color='k', grid=True)

# 如果当天股价上涨，标出卖出信号，用倒三角表示
plt.scatter(df['收盘'].loc[df["交易信号"] == 1].index,
            df['收盘'][df["交易信号"] == 1],
            marker='v', s=80, c='g')

# 如果当天股价下跌给出买入信号，用正三角表示
plt.scatter(df['收盘'].loc[df["交易信号"] == 0].index,
            df['收盘'][df["交易信号"] == 0],
            marker='^', s=80, c='r')

# 将图像进行展示
plt.show()