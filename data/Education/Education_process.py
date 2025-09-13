# Get the script directory 
#data obtained from factnameh
import os
from turtle import color
script_dir = os.path.dirname(os.path.abspath(__file__))

#import libraries
import pandas as pd
import numpy as np
import json

#import data from JSON
def load_education_data_from_json(json_file_path):
    """Load education data from JSON file and convert to DataFrame"""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    # Extract education data from JSON structure
    education_records = json_data['education_data']
    
    # Convert to DataFrame
    df = pd.DataFrame(education_records)
    
    # Rename columns to match original CSV structure
    df = df.rename(columns={'students': 'Students', 'persian_year': 'year'})
    
    return df

# Load data from JSON instead of CSV
json_file_path = os.path.join(script_dir, 'data.json')
data = load_education_data_from_json(json_file_path)

# plot time series of accidents
import matplotlib.pyplot as plt

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
plt.plot(data.index, data['Students'], marker='o', linestyle='-', color='blue', label='Students')
plt.title('Number of Students Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Students')
plt.grid()
plt.legend()


plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'students_analysis.png'), dpi=300, bbox_inches='tight')
print("Plot saved as 'students_analysis.png'")
# plt.show()  # Comment out for headless environments

# Test the stationarity of the time series using Augmented Dickey-Fuller test
from statsmodels.tsa.stattools import adfuller
#drop the first row with NaN values in  students
data = data.dropna(subset=['Students'])

print(f"Data shape after dropping NaN: {data.shape}")
print(f"Available years: {data['year'].min()} to {data['year'].max()}")
print(f"Available Gregorian years: {data['gregorian_year'].min()} to {data['gregorian_year'].max()}")

#remove the data before covid (2019) - use Gregorian year for filtering
data_before_filter = data.copy()
data = data[data['gregorian_year'] >= 2019]

print(f"Data shape after filtering for years >= 2019: {data.shape}")
if data.empty:
    print("No data available after 2019. Using all available data instead.")
    data = data_before_filter

def test_stationarity(timeseries):
    # Perform Augmented Dickey-Fuller test
    result = adfuller(timeseries)
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print(f'   {key}: {value}')

#change the type of Students from integer to float
data['Students'] = data['Students'].astype(float)

# Test stationarity for Students
print("Stationarity Test for Students:")
test_stationarity(data['Students'])

#p value analysis - p is small < 0.05 so we can reject the null hypothesis of non-stationarity so we do not need to difference the series

#plot differenced series and ACF and PACF and original series
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf 
plt.figure(figsize=(12,12))

# Calculate appropriate number of lags
max_lags_acf = min(4, len(data)-1)
max_lags_pacf = max(1, len(data)//2 - 1)  # PACF requires lags < 50% of sample size

plt.subplot(3, 2, 1)
plt.plot(data.index, data['Students'], marker='o', linestyle='-', color='blue', label='Students')
plt.title('Original Students Series')
plt.xlabel('Year')
plt.ylabel('Number of Students')
plt.grid()
plt.legend()

plt.subplot(3, 2, 2)
if len(data) > 2:
    plot_acf(data['Students'], ax=plt.gca(), lags=max_lags_acf)
    plt.title('ACF of Original Students Series')
else:
    plt.text(0.5, 0.5, 'Insufficient data for ACF', ha='center', va='center', transform=plt.gca().transAxes)
    plt.title('ACF of Original Students Series')

plt.subplot(3, 2, 4)
if len(data) > 2:
    plot_acf(data['Students_diff'], ax=plt.gca(), lags=max_lags_acf)
    plt.title('ACF of Differenced Students Series')
else:
    plt.text(0.5, 0.5, 'Insufficient data for ACF', ha='center', va='center', transform=plt.gca().transAxes)
    plt.title('ACF of Differenced Students Series')

plt.subplot(3, 2, 5)
if max_lags_pacf >= 1:
    plot_pacf(data['Students_diff'], ax=plt.gca(), lags=max_lags_pacf)
    plt.title('PACF of Differenced Students Series')
else:
    plt.text(0.5, 0.5, 'Insufficient data for PACF', ha='center', va='center', transform=plt.gca().transAxes)
    plt.title('PACF of Differenced Students Series')

plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'students_acf_pacf.png'), dpi=300, bbox_inches='tight')
print("Plot saved as 'students_acf_pacf.png'")
# plt.show()  # Comment out for headless environments

# Analyze the p-value to determine if differenced series is stationary
print(f"\nNote: With only {len(data)} data points after filtering, the analysis has limited statistical power.")

# fit ARIMA model to the  series
from statsmodels.tsa.arima.model import ARIMA
# Fit ARIMA model (p=1, d=1, q=0) based on ACF and PACF plots
model = ARIMA(data['Students'], order=(1, 1, 0))
model_fit = model.fit()
print(model_fit.summary())
# Forecast the next 3 years and plot the results with confidence intervals
forecast = model_fit.get_forecast(steps=3)

# Create proper forecast index - should start from next year after data ends
last_year = data.index[-1].year
forecast_years = [last_year + i for i in range(1, 4)]  # Next 3 years
forecast_index = pd.to_datetime([f'{year}-01-01' for year in forecast_years])

forecast_series = pd.Series(forecast.predicted_mean, index=forecast_index)
forecast_ci = forecast.conf_int()

print(f"Data ends at: {data.index[-1]}")
print(f"Forecast starts at: {forecast_index[0]}")
print(f"Forecast years: {[year for year in forecast_years]}")
# Plot historical and forecasted 
plt.figure(figsize=(12,6))
plt.plot(data.index, data['Students'], marker='o', linestyle='-', color='red', label='Historical')  

plt.plot(forecast_index, forecast_series, marker='o', linestyle='--', color='blue', label='Forecasted'  , markersize=8)
plt.fill_between(forecast_index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='blue', alpha=0.2, label='Confidence Interval')
# Calculate and plot unconditional mean
unconditional_mean = data['Students'].mean()
plt.axhline(y=unconditional_mean, color='green', linestyle=':', linewidth=2, label=f'Unconditional Mean ({unconditional_mean:.1f})')

# Add forecast values as text annotations
for i, (date, value) in enumerate(zip(forecast_index, forecast_series)):
    persian_year = date.year - 621
    plt.annotate(f'{persian_year}\n{value:.0f}', 
                xy=(date, value), 
                xytext=(10, 10), 
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='blue', alpha=0.3),
                fontsize=9)
plt.title('Forecast of Students for Next 3 Years')
plt.xlabel('Year')
plt.ylabel('Number of Students')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'students_forecast.png'), dpi=300, bbox_inches='tight')
print("Plot saved as 'students_forecast.png'")
# plt.show()  # Comment out for headless environments
# Extract forecasted values for summary statistics
forecasted_students = forecast_series.values
unconditional_mean_students = unconditional_mean    

# Print summary statistics
print(f"\nForecast Summary:")
print(f"Historical mean students per year: {unconditional_mean_students:.0f}")
print(f"Forecasted students average (next 3 years): {np.mean(forecasted_students):.0f}")
print(f"Expected change from historical mean: {np.mean(forecasted_students) - unconditional_mean_students:+.0f}")

if np.mean(forecasted_students) > unconditional_mean_students:
    print("📈 Forecast indicates student enrollment above historical average")
else:
    print("📉 Forecast indicates student enrollment below historical average")

# Export results to JSON for website integration
def export_results_to_json():
    """Export analysis results to JSON for website consumption"""
    results = {
        "metadata": {
            "analysis_date": pd.Timestamp.now().isoformat(),
            "data_source": "factnameh",
            "analysis_type": "ARIMA_forecast",
            "model_order": "(1,1,0)"
        },
        "historical_data": {
            "years": data['year'].tolist(),
            "gregorian_years": data['gregorian_year'].tolist(),
            "students": data['Students'].tolist(),
            "mean_students": float(unconditional_mean_students),
            "data_points": len(data)
        },
        "forecast": {
            "forecast_years": forecast_years,
            "forecasted_students": forecasted_students.tolist(),
            "forecast_mean": float(np.mean(forecasted_students)),
            "confidence_intervals": {
                "lower": forecast_ci.iloc[:, 0].tolist(),
                "upper": forecast_ci.iloc[:, 1].tolist()
            }
        },
        "analysis_summary": {
            "historical_mean": float(unconditional_mean_students),
            "forecast_mean": float(np.mean(forecasted_students)),
            "expected_change": float(np.mean(forecasted_students) - unconditional_mean_students),
            "trend": "above_average" if np.mean(forecasted_students) > unconditional_mean_students else "below_average"
        }
    }
    
    # Save to JSON file
    output_path = os.path.join(script_dir, 'education_analysis_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis results exported to: {output_path}")
    return results

# Export the results
analysis_results = export_results_to_json()