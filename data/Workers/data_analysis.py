import os

script_dir = os.path.dirname(os.path.abspath(__file__))

#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#load data
data = pd.read_csv(os.path.join(script_dir, 'data.csv'))

# Convert Persian year to Gregorian year for proper datetime handling
# Persian year 1395 ≈ 2016 CE, so we add 621 to convert
data['gregorian_year'] = data['year'] + 621
data['year_datetime'] = pd.to_datetime(data['gregorian_year'], format='%Y')
data.set_index('year_datetime', inplace=True)
data.sort_index(inplace=True)
print(data.head())
#plot time series of students
plt.figure(figsize=(12,8))

# Create subplot for deaths and wounded
plt.plot(data.index, data['death'], marker='o', linestyle='-', color='blue', label='Workers Died')
plt.title('Number of Workers Died Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Workers Died')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'workers_analysis.png'), dpi=300, bbox_inches='tight')
print("Plot saved as 'workers_analysis.png'")


#test stationarity with adfuller for growth rate of deaths
from statsmodels.tsa.stattools import adfuller

result = adfuller(data['death'].diff().dropna())
print('ADF Statistic:', result[0])
print('p-value:', result[1])
'''''
#plot the growth rate of deaths
plt.figure(figsize=(12,8))
plt.plot(data.index, data['death'].diff(), marker='o', linestyle='-', color='orange', label='Growth Rate of Workers Died')
plt.title('Growth Rate of Workers Died Over Years')
plt.xlabel('Year')
plt.ylabel('Growth Rate of Workers Died')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'workers_growth_rate.png'), dpi=300, bbox_inches='tight')
print("Plot saved as 'workers_growth_rate.png'")

'''''

# Limited number of observations, so we will not do extensive modeling here !!!

#we use the last value to forecast the next year
last_value = data['death'].iloc[-1]
print(f"Last recorded number of workers died: {last_value}")
next_year_forecast = last_value  # Naive forecast
print(f"Forecasted number of workers died for next year: {next_year_forecast}")
