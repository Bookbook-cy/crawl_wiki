import yfinance as yf
import matplotlib.pyplot as plt
# 获取苹果公司股票的历史数据
data = yf.download('AAPL', start='2022-01-01', end='2025-03-20')
# 计算短期和长期移动平均线
data['Short_MA'] = data['Close'].rolling(window=40).mean()
data['Long_MA'] = data['Close'].rolling(window=100).mean()
# 初始化信号列
data['Signal'] = 0

# 当短期均线超过长期均线时，生成买入信号
data.loc[data['Short_MA'] > data['Long_MA'], 'Signal'] = 1

# 当短期均线低于长期均线时，生成卖出信号
data.loc[data['Short_MA'] < data['Long_MA'], 'Signal'] = -1
# 计算每日收益率
data['Daily_Return'] = data['Close'].pct_change()

# 计算策略收益
data['Strategy_Return'] = data['Daily_Return'] * data['Signal'].shift(1)


# 绘制股票价格和移动平均线
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['Short_MA'], label='40-Day MA')
plt.plot(data['Long_MA'], label='100-Day MA')
plt.legend()
plt.title('AAPL Stock Price and Moving Averages')
plt.show()

# 绘制策略的累积收益
data['Cumulative_Strategy_Return'] = (1 + data['Strategy_Return']).cumprod()
plt.figure(figsize=(14, 7))
plt.plot(data['Cumulative_Strategy_Return'], label='Strategy Return')
plt.legend()
plt.title('Cumulative Strategy Return')
plt.show()
