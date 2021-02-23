# Import packages
import matplotlib.pyplot as plt
import pandas as pd
from pandas_profiling import ProfileReport
from alpha_vantage.timeseries import TimeSeries

# API connection to Alpha Vantage API
API_key = 'YTYPBTRIFHXSB2W2'
ts = TimeSeries(key=API_key, output_format='pandas')
data = ts.get_daily_adjusted('TSLA')

# Initial Dataframe
df=data[0]

# To display HTML report (inline for Jupyter)
profile = ProfileReport(df, title="Pandas Profiling Report")
profile.to_notebook_iframe()


# Raw graph of all relevant features, irrelevent are dividends and splits - for test case at least (TSLA)
fig, ax = plt.subplots()
plt.figure(figsize=(20,10))

ax.plot(df['1. open'], label='Open')
ax.plot(df['2. high'], label='High')
ax.plot(df['3. low'], label='Low')
ax.plot(df['4. close'], label='Close')
ax.plot(df['5. adjusted close'], label='Adjusted Close')

plt.legend()
plt.show()



#Creating and Plotting Moving Averages
df["SMA5"] = df['5. adjusted close'].rolling(window=5).mean()
df["SMA20"] = df['5. adjusted close'].rolling(window=20).mean()
df['exma'] = df['5. adjusted close'].ewm(halflife=0.5, min_periods=20).mean()
plt.figure(figsize=(20,10))
plt.plot(df['SMA1'], 'g--', label="SMA1")
plt.plot(df['SMA2'], 'r--', label="SMA2")
plt.plot(df['5. adjusted close'], label="close")
plt.legend()
plt.title(f"{ticker} Moving Averages")
plt.show()


#Bollinger Bands
df['middle_band'] = df['5. adjusted close'].rolling(window=20).mean()
df['upper_band'] = df['5. adjusted close'].rolling(window=20).mean() + df['5. adjusted close'].rolling(window=20).std()*2
df['lower_band'] = df['5. adjusted close'].rolling(window=20).mean() - df['5. adjusted close'].rolling(window=20).std()*2
plt.figure(figsize=(20,10))
plt.plot(df['upper_band'], 'g--', label="upper")
plt.plot(df['middle_band'], 'r--', label="middle")
plt.plot(df['lower_band'], 'y--', label="lower")
plt.plot(df['5. adjusted close'], label="close")
plt.legend()
plt.title(f"{ticker} Bollinger Bands")
plt.show()

plt.figure(figsize=(20,10))
plt.plot(df['upper_band'].iloc[-200:], 'g--', label="upper")
plt.plot(df['middle_band'].iloc[-200:], 'r--', label="middle")
plt.plot(df['lower_band'].iloc[-200:], 'y--', label="lower")
plt.plot(df['5. adjusted close'].iloc[-200:], label="close")
plt.legend()
plt.title(f"{ticker} Bollinger Bands")
plt.show()