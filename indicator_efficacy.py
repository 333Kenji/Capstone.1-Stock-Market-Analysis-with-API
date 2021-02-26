import matplotlib.pyplot as plt
import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries
plt.style.use('bmh')


# API Connection
API_key = 'YTYPBTRIFHXSB2W2'
ts = TimeSeries(key=API_key, output_format='pandas')



# Initial Dataframe
ticker='TSLA'
data = ts.get_daily_adjusted(ticker)
df=data[0]
df=df.transpose()
df.rename(index={'1. open':'Open', '2. high':'High', '3. low':'Low', '4. close':'Close', '5. adjusted close':'Adjusted Close', '6. volume':'Volume', '7. dividend amount':'Dividend Amount', '8. split coefficient':'Split Coefficient'}, inplace=True)
df=df.transpose()

### To display HTML report (inline for Jupyter)
# profile = ProfileReport(df, title="Pandas Profiling Report")
# profile.to_notebook_iframe()


# Capture And Reset DF Index
df1=pd.read_csv('https://raw.githubusercontent.com/333Kenji/Technical-Indicator-Efficacy/master/Data/df.csv')
df1=df1[::-1]
df1 = df1.set_index(pd.DatetimeIndex(df1['date'].values))


# Inital Plot of All Price Data
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df1['Open'], label='Open')
ax.plot(df1['High'], label='High')
ax.plot(df1['Low'], label='Low')
ax.plot(df1['Close'], label='Close')
ax.plot(df1['Adjusted Close'], label='Adjusted Close')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.show()

# Volumn Plot
fig, ax = plt.subplots(figsize=(10,5))
plt.xticks(rotation=45)
ax.plot(df1['Volume'])


### MACD Indicator ###


# Long and Short Moving Averages
EMA12 = df1.Close.ewm(span=12, adjust=False).mean()
EMA26 = df1.Close.ewm(span=26, adjust=False).mean()
# Calculate the MACD
MACD = EMA12 - EMA26
# Generate The Signal
signal = MACD.ewm(span=9, adjust=False).mean()

# Plotting MACD Against Signal
plt.figure(figsize=(20,10))
plt.plot(df1.index, MACD, label = f'{ticker} MACD', color='red', alpha=.4)
plt.plot(df1.index, signal, label='Signal Line', color='blue',alpha=.4)
plt.legend(loc='upper left')
plt.xticks(rotation=45)
plt.show()


# Add MACD And Signal to DF
df1['MACD'] = MACD
df1['Signal_Ind'] = signal


# Calculate MACD Score
def score(signal):
    Buy = []
    Sell = []
    flag=bool
    for i in range(0, len(signal)):
        if signal['MACD'][i] > signal['Signal_Ind'][i]:
            Sell.append(np.nan)
            if flag != True:
                Buy.append(signal['Close'][i])
                flag=True
            else:
                Buy.append(np.nan)
        elif signal['MACD'][i] < signal['Signal_Ind'][i]:
            Buy.append(np.nan)
            if flag != False:
                Sell.append(signal['Close'][i])
                flag=False
            else:
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)
    return (Buy, Sell)


# Add Scores To DF
a = score(df1)
df1['Buy_Sig_Price'] = a[0]
df1['Sell_Sig_Price']= a[1]


# Plot Scores
plt.figure(figsize=(10,5))
plt.scatter(df1.index, df1['Buy_Sig_Price'], color='green', label='Buy', marker='^', alpha=1)
plt.scatter(df1.index, df1['Sell_Sig_Price'], color='red', label='Sell', marker='v', alpha=1)

plt.plot(df1['Close'], label='Closing Price', alpha=.4)
plt.title('Closing Buy Sell Sigs')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.xticks(rotation=45)
plt.show()





#Bollinger Bands
df1['middle_band'] = df1['Adjusted Close'].rolling(window=20).mean()
df1['upper_band'] = df1['Adjusted Close'].rolling(window=20).mean() + df1['Adjusted Close'].rolling(window=20).std()*2
df1['lower_band'] = df1['Adjusted Close'].rolling(window=20).mean() - df1['Adjusted Close'].rolling(window=20).std()*2
plt.figure(figsize=(20,10))
plt.plot(df1['upper_band'], 'g--', label="upper")
plt.plot(df1['middle_band'], 'r--', label="middle")
plt.plot(df1['lower_band'], 'y--', label="lower")
plt.plot(df1['Adjusted Close'], label="close")
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.title(f"{ticker} Bollinger Bands")
plt.show()

plt.figure(figsize=(20,10))
plt.plot(df1['upper_band'].iloc[-200:], 'g--', label="upper")
plt.plot(df1['middle_band'].iloc[-200:], 'r--', label="middle")
plt.plot(df1['lower_band'].iloc[-200:], 'y--', label="lower")
plt.plot(df1['Adjusted Close'].iloc[-200:], label="close")
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.title(f"{ticker} Bollinger Bands")
plt.show()

