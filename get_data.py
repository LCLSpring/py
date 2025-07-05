import akshare as ak

stock_sse_summary_df = ak.stock_sse_summary()
print("we got 上海证券交易所股票总览：\n",stock_sse_summary_df)

stock_szse_summary_df = ak.stock_szse_summary(date="20200630")
print("we got 深圳证券交易所20250704 证券类别统计信息 \n", stock_szse_summary_df)