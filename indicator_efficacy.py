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