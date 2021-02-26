![alt text](https://github.com/333Kenji/Technical-Indicator-Efficacy/blob/master/Images/cover_imagev2.jpg)
# Technical Indicator Reliability #

For this capstone I've compared the predictive accuracy of the Moving Average Convergence Divergence ([MACD](https://en.wikipedia.org/wiki/MACD "Named link title")) technical indicator across the performance of multiple stocks and ETFs in order to determine the likelihood that investment suggestions (to buy) are indeed correct. That is, if the MACD indicator suggests that the price will increase the next day, how likely is it that it will indeed increase.

- - - -
## EDA Process ##

For this project I was determined to remain true to the EDA process by placing emphasis on visualizing the raw data first and foremost, and then allow myself to to visually pick out remarkable features and relationships before constructing any models or taking on any assumptions about what models or means of analysis to use or what features to ommit to synthesize. Using matplotlib and pandas profiler I noticed right away that the dividend and split coefficients where constants, i.e. flat lines, across each ticker's table. Moreover, the volume feature exists on a scale far outside of price data features which all formed a cluster of similarly scaled data.

## Pipeline ##

I used the Alpha Vantage API which provides price, volume, and even technical indicator data for stocks, ETFs, and cryptocurrencies via endpoints, specific queries that return tabular data for a specific asset.
Once this data was imported to my local machine, in order to avoid hitting the 5 query per minute rate limit I saved each table to its own CSV file which was then uploaded to my projects Data directory on GitHub and dre data from that source.
- - - -
## Raw Data ##
From that initial analysis of the raw data I determined the two constant features to be both redundant and irrelevant, so they were discarded, while volume was retained as it is a feature I'll make use of in future iterations of this project to develop additional technical indicators.

```
API Connection
API_key = 'YTYPBTRIFHXSB2W2'
ts = TimeSeries(key=API_key, output_format='pandas')
```


The API I used [Alpha Vantage](https://www.alphavantage.co/ "Named link title") returns a table of features for each asset, indexed by date:
* opening,
* closing,
* adjusted closing,
* daily high and low prices,
* the assets volume,
* dividend amount
* split coefifient

As an API, this source relayed clean data though some features seemed  unnecessary at first glance. After researching the non-price related features I came across a point of potential concern since Tesla's stock was split last year, which would be reflected as a retroactive correction of the closing  price. Fortunately the endpoint only retrieves data, by default, for the past 100 days so any differences between the two features were not present in my data.

![alt_text](https://github.com/333Kenji/Technical-Indicator-Efficacy/blob/master/Images/Raw_Table.png)

![alt text](https://github.com/333Kenji/Technical-Indicator-Efficacy/blob/master/Images/Raw_ABNB.png)
- - - -



## The MACD ##
The MACD is composed of two trendlines, by convention 2 standard deviations above and below a 9 day weighted average.
![ARKK Invest MACD](https://github.com/333Kenji/Technical-Indicator-Efficacy/blob/master/Images/MACD_ARKK.png)
![AMC MACD](https://github.com/333Kenji/Technical-Indicator-Efficacy/blob/master/Images/MACD_AMC.png)

<details>
```
# Long and Short Moving Averages
def MACD_Indicator(key):
    df1=tables[key]
    EMA12 = df1.Close.ewm(span=12, adjust=False).mean()
    EMA26 = df1.Close.ewm(span=26, adjust=False).mean()
# Calculate the MACD
    MACD = EMA12 - EMA26
# Generate The Signal
    signal = MACD.ewm(span=9, adjust=False).mean()
# Add MACD And Signal to DF
    tables[key]['MACD'] = MACD
    tables[key]['Signal_Ind'] = signal
    return
MACD_Indicator(ticker)
```
</details>

- - - -
Once the MACD feature data was added to each tickers table I then wrote a function to calculate how often the MACD suggested the price would increase the next day.

<details>

     
```
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
```
</details>
And plotted these as well as Sell suggestions along the assets closing price:

![AMC Suggested Buy Points](https://github.com/333Kenji/Technical-Indicator-Efficacy/blob/master/Images/Suggestions_AMC.png)

![ARKK Invest Suggested Buy Points](https://github.com/333Kenji/Technical-Indicator-Efficacy/blob/master/Images/Suggestions_ARKK.png)



From there I was able to compose a new table of all times the MACD's suggestion of a buy opportunity to occure the following day and observe and compare performance across the assets in my study.
![MACD Scores Across](https://github.com/333Kenji/Technical-Indicator-Efficacy/blob/master/Images/MACD_Scores_Across.png)

![MACD Scores For Each](https://github.com/333Kenji/Technical-Indicator-Efficacy/blob/master/Images/MACD_Scores_Each.png)




---
# Further Analysis: #
- Increase Number of Tickers To Test The MACD Against
- Increase The Window For Backtesting The MACD Against, i.e. Increase The Window From The Day After Suggestion To Buy To Several Days, Weeks, or Months.
- Investigate Thresholds Above and Below a 2% Day Over Day Increase In Asset Price

---