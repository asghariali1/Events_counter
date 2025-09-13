import pandas as pd
import os

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

#import the data
data = pd.read_csv(os.path.join(script_dir, 'data.csv'))

import numpy as np


# plot time series of accidents
import matplotlib.pyplot as plt

# Convert Persian year to Gregorian year for proper datetime handling
# Persian year 1395 ≈ 2016 CE, so we add 621 to convert
data['gregorian_year'] = data['year'] + 621
data['year_datetime'] = pd.to_datetime(data['gregorian_year'], format='%Y')
data.set_index('year_datetime', inplace=True)
data.sort_index(inplace=True)


#save a plot of the time series
plt.figure(figsize=(12,8))
plt.plot(data.index, data['Deaths'], label='Deaths')
plt.title('Time Series of Air Pollution Related Deaths')
plt.xlabel('Year')
plt.ylabel('Number of Deaths')
plt.legend()
plt.grid()
plt.savefig(os.path.join(script_dir, 'air_pollution.png'))
plt.close()

#From ther plot we can see that the time series is not stationary
# Test the stationarity of the time series using Augmented Dickey-Fuller test
from statsmodels.tsa.stattools import adfuller

result = adfuller(data['Deaths'].dropna())
print('ADF Statistic:', result[0])
print('p-value:', result[1])

# create th growth rate column
data['Growth_Rate'] = data['Deaths'].pct_change() * 100
data['Growth_Rate'] = data['Growth_Rate'].replace([np.inf, -np.inf], np.nan)
data['Growth_Rate'] = data['Growth_Rate'].fillna(0)
data['Growth_Rate'] = data['Growth_Rate'].round(2)

#plot the growth rate
plt.figure(figsize=(12,8))
plt.plot(data.index, data['Growth_Rate'], marker='o', linestyle='-', color='orange', label='Growth Rate (%)')
plt.title('Growth Rate of Air Pollution Related Deaths')
plt.xlabel('Year')
plt.ylabel('Growth Rate (%)')
plt.axhline(0, color='gray', linestyle='--')
plt.legend()
plt.grid()
plt.savefig(os.path.join(script_dir, 'air_pollution_growth_rate.png'))
plt.close()

# Forcasting using OLS regression
import statsmodels.api as sm

X = data.index.year.values.reshape(-1, 1)  # Years as the feature
y = data['Deaths'].values  # Deaths as the target variable

X = sm.add_constant(X)  # Adds a constant term to the predictor

model = sm.OLS(y, X, missing='drop').fit()

#print the regression results
print(model.summary())


# Forecast for the next year 
next_year = pd.DataFrame({'const': 1, 'year': [data.index.year.max() + 1]})
forecast = model.predict(next_year)
print(f"Forecasted Deaths for {next_year['year'].values[0]}: {int(round(forecast[0]))}")
# Save the forecast to a text file
with open(os.path.join(script_dir, 'forecast.txt'), 'w') as f:
    f.write(f"Forecasted Deaths for {next_year['year'].values[0]}: {int(round(forecast[0]))}\n")
# End of the forecast
#plot the  regression line and the original time series and forcaseted point
plt.figure(figsize=(12,8))
#Only plot after 2020
plt.plot(data.index, data['Deaths'], marker='o', linestyle='-', color='blue', label='Actual Deaths')
plt.plot(data.index, model.predict(X), color='red', linestyle='--', label='Regression Line')

# Convert forecast year to datetime to match the data index
forecast_datetime = pd.to_datetime(next_year['year'].values[0], format='%Y')
plt.scatter(forecast_datetime, forecast, color='green', s=100, label='Forecasted Point')

plt.title('OLS Regression and Forecast of Air Pollution Related Deaths')
plt.xlabel('Year')
plt.ylabel('Number of Deaths')
plt.legend()
plt.grid()
plt.savefig(os.path.join(script_dir, 'air_pollution_regression_forecast.png'))
plt.close()