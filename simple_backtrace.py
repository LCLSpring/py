import akshare as ak
import numpy as np
from matplotlib import pyplot as plt

# 比亚迪 A 股的股票代码：002594（深市）
stock_code = "002594"

# 获取历史行情数据
df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date="20250101", end_date="20250630", adjust="qfq")
df = df[["日期", "收盘", "涨跌额"]]
df["交易信号"] = np.where(df["涨跌额"] >= 0, 0, 1)

# 初始化
df["下单量"] = 0
cum_position = 0  # 当前持仓

# 应用逻辑：只有在“允许的前提下”才能下单
for i in range(1, len(df)):
    signal = df.at[i, "交易信号"]
    prev_signal = df.at[i - 1, "交易信号"]
    # 检查是否信号切换（买→卖 或 卖→买）
    if signal != prev_signal:
        order = (signal - prev_signal) * 100  # 1→0为卖 -100；0→1为买 100
        # 判断是否可以卖（不能卖空）
        if cum_position + order >= 0:
            df.at[i, "下单量"] = order
            cum_position += order
# 考虑到股价较高，我们初始给小瓦20万元人民币让她去交易
initial_cash = 200000.00

# 增加一个字段，代表小瓦交易的股票的市值
df['交易股票价值'] = df['下单量'] * df['收盘']

# 持仓股票的数量变化×现价，就是小瓦交易产生的现金流
# 用初始资金减去现金流变化的累加，就是小瓦剩余的现金
df['剩余现金'] = initial_cash - df['交易股票价值'].cumsum()

# 而股票的市值加上剩余的现金，就是小瓦的总资产
df['总资产'] = df['剩余现金'] + df['下单量'].cumsum() * df['收盘']

print(df)

# 我们用图形来进行展示
# 设置图形的尺寸是10×6
plt.figure(figsize=(10, 6))

# # 分别绘制总资产和持仓股票市值的变化
plt.plot(df['总资产'])
plt.plot(df['下单量'].cumsum() * df['收盘'], '--', label='stock value')

# # 增加网格，调整一下图注的位置，就可以显示图像了
plt.grid()
plt.legend(loc='center right')
plt.show()
