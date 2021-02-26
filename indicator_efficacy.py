import matplotlib.pyplot as plt
import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries
plt.style.use('bmh')

null_hyp = .8

# API Connection
API_key = 'YTYPBTRIFHXSB2W2'
ts = TimeSeries(key=API_key, output_format='pandas')

# Initialize Dataframe - DO NOT FUNCTIONALIZE BECAUSE RATE LIMITS
ticker='UBER'
data = ts.get_daily_adjusted(ticker)
df=data[0]
df=df.transpose()
df.rename(index={'1. open':'Open', '2. high':'High', '3. low':'Low', '4. close':'Close', '5. adjusted close':'Adjusted Close', '6. volume':'Volume', '7. dividend amount':'Dividend Amount', '8. split coefficient':'Split Coefficient'}, inplace=True)
df=df.transpose()


#Save DF to CSV
df.to_csv(f'Data/{ticker}.csv', index=True)

### FOR INITIAL EDA: To display HTML report (inline for Jupyter)
# profile = ProfileReport(df, title="Pandas Profiling Report")
# profile.to_notebook_iframe()

tickers = ['ABNB', 'AMC', 'ARKK', 'GME', 'PLTR', 'SPY', 'TSLA', 'UBER']

tables = read_csvs(tickers)
tables.keys()

# Inital Plot of All Price Data
def raw_charts(key):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(tables[key]['Open'], label='Open')
    ax.plot(tables[key]['High'], label='High')
    ax.plot(tables[key]['Low'], label='Low')
    ax.plot(tables[key]['Close'], label='Close')
    ax.plot(tables[key]['Adjusted Close'], label='Adjusted Close')
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f"{key} Raw Price Data")
    plt.legend(loc='upper left')
    return plt.show()

for t in tables.keys():
    raw_charts(t)
    
    
### MACD Indicator ###
ticker = df1 = 'UBER'


# Long and Short Moving Averages
def MACD_Indicator(key):
    df1 = tables[key]
    EMA12 = df1.Close.ewm(span=12, adjust=False).mean()
    EMA26 = df1.Close.ewm(span=26, adjust=False).mean()
# Calculate the MACD
    MACD = EMA12 - EMA26
# Generate The Signal
    signal = MACD.ewm(span=9, adjust=False).mean()
# Add MACD And Signal to DF
    tables[key]['MACD'] = MACD
    tables[key]['Signal_Ind']=signal
    return
MACD_Indicator(ticker)



# Plotting MACD Against Signal

df1 = tables[ticker]
plt.figure(figsize=(20,10))
plt.plot(df1.index, df1['MACD'], label = f'{ticker} MACD', color='red', alpha=.4)
plt.plot(df1.index, df1['Signal_Ind'], label='Signal Line', color='blue',alpha=.4)
plt.legend(loc='upper left')
plt.xlabel('Date')
plt.ylabel('Strength')
plt.title(f"{key} MACD And 9 Day Signal")
plt.xticks(rotation=45)
plt.show()


# Calculate MACD Score
def score(signal):
    Buy = []
    Sell = []
    flag = bool
    for i in range(0, len(signal)):
        if signal['MACD'][i] > signal['Signal_Ind'][i]:
            Sell.append(np.nan)
            if flag != True:
                Buy.append(signal['Close'][i])
                flag = True
            else:
                Buy.append(np.nan)
        elif signal['MACD'][i] < signal['Signal_Ind'][i]:
            Buy.append(np.nan)
            if flag != False:
                Sell.append(signal['Close'][i])
                flag = False
            else:
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)
    return (Buy, Sell)


# Add Scores To DF
a = score(df1)
df1['Buy_Sig_Price'] = a[0]
df1['Sell_Sig_Price'] = a[1]



# Plot Scores
def Ind_Suggestion():
    plt.figure(figsize=(10,5))
    plt.scatter(df1.index, df1['Buy_Sig_Price'], color='green', label='Buy', marker='^', alpha=1)
    plt.scatter(df1.index, df1['Sell_Sig_Price'], color='red', label='Sell', marker='v', alpha=1)

    plt.plot(df1['Close'], label='Closing Price', alpha=.4)
    plt.title('Closing Buy Sell Sigs')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f"{ticker} Indicator Suggestions")
    plt.legend(loc='upper left')
    plt.xticks(rotation=45)
    return plt.show()

Ind_Suggestion()


# Suggestion Strength
def suggestion_accuracy():
    suggestions = 0
    correct = 0
    for Day_Prior, closing_price, Day_After, next_day_price in zip(df1.index, df1['Close'] ,df1.index[1:-1], df1['Buy_Sig_Price'][1:-1]):
        if closing_price < next_day_price:
            suggestions += 1
        if closing_price*1.02 < next_day_price:
            correct += 1
    return suggestions, correct, correct/suggestions


suggestion, correct, score = suggestion_accuracy()


ABNB = (2, 2, 1.0)
AMC = (3, 2, 0.6666666666666666)
ARKK = (5, 3, 0.6)
GME = (5, 4, 0.8)
PLTR = (4, 4, 1.0)
SPY = (5, 0, 0.0)
TSLA = (5, 5, 1.0)
UBER = (5, 3, 0.6)

scores = np.array([ABNB, AMC, ARKK, GME, PLTR, SPY, TSLA, UBER])
ScoresDF = pd.DataFrame(scores, index=tables.keys(), columns=['Suggestions', 'Correct','null'])
Scores = ScoresDF.iloc[:, 0:2]

pd.plotting.scatter_matrix(Scores, figsize=(6, 6), s=100)
ScoresDF.iloc[:, 0:2].plot(kind="line", figsize=(10, 5), title='MACD Sores Across Tickers')
ScoresDF.iloc[:, 0:2].plot(kind="bar", figsize=(10, 5), title='Scores For Each Ticker')


def summary():
    
    sum_suggestions = sum(ScoresDF.iloc[:, 0])
    sum_correct = sum(ScoresDF.iloc[:, 1])
    Indicator_Str = sum_correct/sum_suggestions
    print(f'{sum_suggestions} Total Suggestions')
    print (f'{sum_correct} Correct Suggestions')
    print (f'{round(Indicator_Str,2)} Total Strength')
    print(f' Indicator Observed Strength Over Null Hypothesis is {Indicator_Str/null_hyp})
    return

summary()