# Import Libraries
%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd
from pandas_profiling import ProfileReport

# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

# API Connection
from alpha_vantage.timeseries import TimeSeries

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


# Captured DF
df1=pd.read_csv('https://raw.githubusercontent.com/333Kenji/Technical-Indicator-Efficacy/master/Data/df.csv')

df1=df1[::-1]
df1.index=df1['date']

ticker='TSLA'

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



#Bollinger Bands
df1['middle_band'] = df1['Adjusted Close'].rolling(window=20).mean()
df1['upper_band'] = df1['Adjusted Close'].rolling(window=20).mean() + df1['Adjusted Close'].rolling(window=20).std()*2
df1['lower_band'] = df1['Adjusted Close'].rolling(window=20).mean() - df1['Adjusted Close'].rolling(window=20).std()*2
plt.figure(figsize=(20,10))
plt.plot(df1['upper_band'], 'g--', label="upper")
plt.plot(df1['middle_band'], 'r--', label="middle")
plt.plot(df1['lower_band'], 'y--', label="lower")
plt.plot(df1['Adjusted Close'], label="close")
plt.legend()
plt.title(f"{ticker} Bollinger Bands")
plt.show()

plt.figure(figsize=(20,10))
plt.plot(df1['upper_band'].iloc[-200:], 'g--', label="upper")
plt.plot(df1['middle_band'].iloc[-200:], 'r--', label="middle")
plt.plot(df1['lower_band'].iloc[-200:], 'y--', label="lower")
plt.plot(df1['Adjusted Close'].iloc[-200:], label="close")
plt.legend()
plt.title(f"{ticker} Bollinger Bands")
plt.show()

