import akshare as ak
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 推荐字体路径（macOS）
font_path = "/System/Library/Fonts/PingFang.ttc"
font_prop = fm.FontProperties(fname=font_path)

# 设置 matplotlib 使用它
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# 设置股票代码（比亚迪 A 股）
stock_code = "002594"

# 时间范围
start_date = "20250601"
end_date = "20250630"

# 获取三种复权数据
df_none = ak.stock_zh_a_hist(symbol=stock_code, period='daily', start_date=start_date, end_date=end_date)
df_qfq = ak.stock_zh_a_hist(symbol=stock_code, period='daily', start_date=start_date, end_date=end_date, adjust="qfq")
df_hfq = ak.stock_zh_a_hist(symbol=stock_code, period='daily', start_date=start_date, end_date=end_date, adjust="hfq")

# 统一时间轴为 index
df_none.set_index("日期", inplace=True)
df_qfq.set_index("日期", inplace=True)
df_hfq.set_index("日期", inplace=True)

# 只提取收盘价
close_none = df_none["收盘"]
close_qfq = df_qfq["收盘"]
close_hfq = df_hfq["收盘"]

# 画图对比
plt.figure(figsize=(12, 6))
plt.plot(close_none, label="原始价格（未复权）")
plt.plot(close_qfq, label="前复权")
plt.plot(close_hfq, label="后复权")
plt.title("比亚迪 2023年1-3月 收盘价对比（三种复权方式）")
plt.xlabel("日期")
plt.ylabel("收盘价（元）")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
