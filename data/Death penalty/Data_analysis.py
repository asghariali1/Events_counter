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
plt.plot(data.index, data['Death penalty'], marker='o', linestyle='-', color='blue', label='Death Penalties')
plt.title('Number of Death Penalties Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Death Penalties')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'death_penalties_analysis.png'), dpi=300, bbox_inches='tight')
print("Plot saved as 'death_penalties_analysis.png'")


#test stationarity with adfuller for growth rate of deaths
from statsmodels.tsa.stattools import adfuller

result = adfuller(data['Death penalty'].diff().dropna())
print('ADF Statistic:', result[0])
print('p-value:', result[1])

#calculating the growth rate of deaths
data['death_growth_rate'] = data['Death penalty'].pct_change()
print(data['death_growth_rate'])

#plot the growth rate of deaths
plt.figure(figsize=(12,8))
plt.plot(data.index, data['death_growth_rate'], marker='o', linestyle='-', color='orange', label='Growth Rate of Death Penalties')
plt.title('Growth Rate of Death Penalties Over Years')
plt.xlabel('Year')
plt.ylabel('Growth Rate of Death Penalties')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'death_penalties_growth_rate.png'), dpi=300, bbox_inches='tight')
print("Plot saved as 'death_penalties_growth_rate.png'")

# ADF test on growth rate
result_growth = adfuller(data['death_growth_rate'].dropna())
print('ADF Statistic for Growth Rate:', result_growth[0])
print('p-value for Growth Rate:', result_growth[1]) 

# data is not stationary
# Limited number of observations, so we will not do extensive modeling here !!!
#we use the last value to forecast the next year
last_value = data['Death penalty'].iloc[-1]
print(f"Last recorded number of death penalties: {last_value}")
next_year_forecast = last_value  # Naive forecast
print(f"Forecasted number of death penalties for next year: {next_year_forecast}")

