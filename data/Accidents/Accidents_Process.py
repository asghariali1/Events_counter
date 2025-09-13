# Get the script directory
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

#import libraries
import pandas as pd
import numpy as np

#import data
data = pd.read_csv(os.path.join(script_dir, 'data_all.csv'))

# plot time series of accidents
import matplotlib.pyplot as plt

# Convert Persian year to Gregorian year for proper datetime handling
# Persian year 1395 ≈ 2016 CE, so we add 621 to convert
data['gregorian_year'] = data['year'] + 621
data['year_datetime'] = pd.to_datetime(data['gregorian_year'], format='%Y')
data.set_index('year_datetime', inplace=True)
data.sort_index(inplace=True)
print(data.head())
#plot time series of accidents
plt.figure(figsize=(12,8))

# Create subplot for deaths and wounded
plt.plot(data.index, data['death'], marker='o', linestyle='-', color='red', label='Deaths')
plt.title('Number of Deaths Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Deaths')
plt.grid()
plt.legend()


plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'accidents_analysis.png'), dpi=300, bbox_inches='tight')
print("Plot saved as 'accidents_analysis.png'")
# plt.show()  # Comment out for headless environments

# Test the stationarity of the time series using Augmented Dickey-Fuller test
from statsmodels.tsa.stattools import adfuller
#drop the first row with NaN values in  death 



def test_stationarity(timeseries):
    # Perform Augmented Dickey-Fuller test
    result = adfuller(timeseries)
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print(f'   {key}: {value}')

# Test stationarity for deaths and wounded
print("Stationarity Test for Deaths:")
test_stationarity(data['death'])

#print("\nStationarity Test for Wounded:")
#test_stationarity(data['wounded'])

#p value of 0.45 for both series, so we cannot reject the null hypothesis of non-stationarity so we need to difference the series
data['death_diff'] = data['death'].diff().dropna()
#drop the first row with NaN values in  death_diff
data = data.dropna(subset=['death_diff'])

print(data.head())
print("Differenced Deaths:")
print(data['death_diff'].head())
#data['wounded_diff'] = data['wounded'].diff().dropna()

print("\nStationarity Test for Differenced Deaths:")
test_stationarity(data['death_diff'])
#print("\nStationarity Test for Differenced Wounded:")
#test_stationarity(data['wounded_diff'])

#plot differenced series and ACF and PACF and original series
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf 
plt.figure(figsize=(12,12))
plt.subplot(3, 2, 1)
plt.plot(data.index, data['death'], marker='o', linestyle='-', color='red', label='Deaths')
plt.title('Original Deaths Series')
plt.xlabel('Year')
plt.ylabel('Number of Deaths')
plt.grid()
plt.legend()
plt.subplot(3, 2, 2)
plot_acf(data['death'], ax=plt.gca(), lags=4)
plt.title('ACF of Original Deaths Series')
plt.subplot(3, 2, 3)
plt.plot(data.index, data['death_diff'], marker='o', linestyle='-', color='blue', label='Differenced Deaths')
plt.title('Differenced Deaths Series')
plt.xlabel('Year')
plt.ylabel('Differenced Number of Deaths')
plt.grid()
plt.legend()
plt.subplot(3, 2, 4)
plot_acf(data['death_diff'], ax=plt.gca(), lags=4)
plt.title('ACF of Differenced Deaths Series')
plt.subplot(3, 2, 5)
plot_pacf(data['death_diff'], ax=plt.gca(), lags=4)
plt.title('PACF of Differenced Deaths Series')
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'deaths_acf_pacf.png'), dpi=300, bbox_inches='tight')
print("Plot saved as 'deaths_acf_pacf.png'")
# plt.show()  # Comment out for headless environments

# the p value is 0.25 so we can reject the null hypothesis of non-stationarity so the differenced series is stationary

# fit ARIMA model to the differenced series
from statsmodels.tsa.arima.model import ARIMA
# Fit ARIMA model (p=1, d=1, q=0) based on ACF and PACF plots
model = ARIMA(data['death_diff'], order=(1, 1, 0))
model_fit = model.fit()
print(model_fit.summary())
# Forecast the next 3 years and plot the results with confidence intervals
forecast = model_fit.get_forecast(steps=3)

# Create proper forecast index - should start from 2025 if data ends at 2024
last_year = data.index[-1].year
forecast_years = [last_year + i for i in range(1, 4)]  # 2025, 2026, 2027
forecast_index = pd.to_datetime([f'{year}-01-01' for year in forecast_years])

forecast_series = pd.Series(forecast.predicted_mean, index=forecast_index)
forecast_ci = forecast.conf_int()

print(f"Data ends at: {data.index[-1]}")
print(f"Forecast starts at: {forecast_index[0]}")
print(f"Forecast years: {[year for year in forecast_years]}")
# Plot first differences (historical and forecasted)
plt.figure(figsize=(12,6))
plt.plot(data.index, data['death_diff'], marker='o', linestyle='-', color='red', label='Historical First Differences')

# Plot forecasted first differences
plt.plot(forecast_index, forecast_series, marker='o', linestyle='--', color='blue', label='Forecasted First Differences', markersize=8)
plt.fill_between(forecast_index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='blue', alpha=0.2, label='Confidence Interval')

# Calculate and plot unconditional mean of first differences
unconditional_mean_diff = data['death_diff'].mean()
plt.axhline(y=unconditional_mean_diff, color='green', linestyle=':', linewidth=2, label=f'Unconditional Mean ({unconditional_mean_diff:.1f})')

# Add forecast values as text annotations
for i, (date, value) in enumerate(zip(forecast_index, forecast_series)):
    persian_year = date.year - 621
    plt.annotate(f'{persian_year}\n{value:.1f}', 
                xy=(date, value), 
                xytext=(10, 10), 
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='blue', alpha=0.3),
                fontsize=9)
plt.title('Forecast of First Differences in Deaths for Next 3 Years')
plt.xlabel('Year')
plt.ylabel('First Difference in Number of Deaths')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'deaths_forecast_diff.png'), dpi=300, bbox_inches='tight')
print("Plot saved as 'deaths_forecast_diff.png'")
# plt.show()  # Comment out for headless environments

# Calculate actual deaths forecast by transforming first differences back to levels
print("\n" + "="*60)
print("DEATHS LEVEL FORECAST (Transformed from First Differences)")
print("="*60)

# Get the last actual death count
last_death_count = data['death'].iloc[-1]
print(f"Last observed death count (2024): {last_death_count}")

# Transform first differences forecast back to death levels
# For each forecast period, add the predicted difference to the cumulative sum
forecasted_deaths = []
current_level = last_death_count

for i, diff_forecast in enumerate(forecast_series):
    current_level += diff_forecast
    forecasted_deaths.append(current_level)
    persian_year = forecast_years[i] - 621
    print(f"Year {persian_year} (CE {forecast_years[i]}): {current_level:.0f} deaths")

forecasted_deaths = np.array(forecasted_deaths)

# Calculate confidence intervals for death levels
forecast_ci_lower = []
forecast_ci_upper = []
current_level_lower = last_death_count
current_level_upper = last_death_count

for i in range(len(forecast_series)):
    current_level_lower += forecast_ci.iloc[i, 0]  # Lower bound
    current_level_upper += forecast_ci.iloc[i, 1]  # Upper bound
    forecast_ci_lower.append(current_level_lower)
    forecast_ci_upper.append(current_level_upper)

# Plot deaths level forecast
plt.figure(figsize=(14,8))

# Plot historical deaths
plt.plot(data.index, data['death'], marker='o', linestyle='-', color='red', 
         label='Historical Deaths', linewidth=2, markersize=6)

# Plot forecasted deaths
plt.plot(forecast_index, forecasted_deaths, marker='s', linestyle='--', color='blue', 
         label='Forecasted Deaths', linewidth=2, markersize=8)

# Plot confidence intervals
plt.fill_between(forecast_index, forecast_ci_lower, forecast_ci_upper, 
                color='blue', alpha=0.2, label='95% Confidence Interval')

# Calculate and plot unconditional mean of deaths
unconditional_mean_deaths = data['death'].mean()
plt.axhline(y=unconditional_mean_deaths, color='green', linestyle=':', linewidth=2, 
           label=f'Historical Mean ({unconditional_mean_deaths:.0f})')

# Add forecast values as text annotations
for i, (date, value) in enumerate(zip(forecast_index, forecasted_deaths)):
    persian_year = date.year - 621
    plt.annotate(f'{persian_year}\n{value:.0f}', 
                xy=(date, value), 
                xytext=(15, 15), 
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='blue', alpha=0.4),
                fontsize=10, fontweight='bold')

plt.title('Deaths Forecast: Historical Data and 3-Year Prediction', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Deaths', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'deaths_level_forecast.png'), dpi=300, bbox_inches='tight')
print(f"\nPlot saved as 'deaths_level_forecast.png'")

# Print summary statistics
print(f"\nForecast Summary:")
print(f"Historical mean deaths per year: {unconditional_mean_deaths:.0f}")
print(f"Forecasted deaths average (next 3 years): {np.mean(forecasted_deaths):.0f}")
print(f"Expected change from historical mean: {np.mean(forecasted_deaths) - unconditional_mean_deaths:+.0f}")

if np.mean(forecasted_deaths) > unconditional_mean_deaths:
    print("⚠️  Forecast indicates deaths above historical average")
else:
    print("✅ Forecast indicates deaths below historical average")