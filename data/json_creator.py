import os
import pandas as pd
import json
from datetime import datetime

#get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read the data 
data = pd.read_csv(os.path.join(script_dir, 'data.csv'))
details_data = pd.read_csv(os.path.join(script_dir, 'details.csv'))
time_series_Iran_data = pd.read_csv(os.path.join(script_dir, 'time_series_Iran.csv'))
time_series_World_data = pd.read_csv(os.path.join(script_dir, 'time_series_World.csv'))
time_series_World_data_sources = pd.read_csv(os.path.join(script_dir, 'world_sources.csv'))

#Accidents data
accidents_rows = data[data['Topic'] == 'Car Accidents'] 

#get the last daily monthly and yearly average (extract first value from Series)
last_daily_avg = int(round(accidents_rows['Daily_Average'].iloc[0]))
last_monthly_avg = int(round(accidents_rows['Monthly_Average'].iloc[0]))
last_yearly_avg = int(accidents_rows['Forecast_Number'].iloc[0])

#get the details of accidents
details_accidents_rows = details_data[details_data['Topic'] == 'Car Accidents']
accidents_title = details_accidents_rows['Title'].iloc[0]
accidents_description = details_accidents_rows['Description'].iloc[0]
accidents_sources = details_accidents_rows['Sources'].iloc[0].split(';')
accidents_sources_links = details_accidents_rows['Sources_Link'].iloc[0].split(';')


#get the time series data for accidents in Iran
time_series_accidents_years = time_series_Iran_data.columns[1:].tolist()  # Exclude the 'Topic' column
time_series_accidents_rows = time_series_Iran_data[time_series_Iran_data['Topic'] == 'Car Accidents']
# Convert to regular Python list with proper int conversion
time_series_accidents_values = [int(val) if pd.notna(val) else None for val in time_series_accidents_rows.iloc[0, 1:].tolist()]
# print(time_series_accidents_values)


# Get the row corresponding to 'Car Accidents' for time series_world_data
time_series_accidents_world_rows = time_series_World_data[time_series_World_data['Topic'] == 'Car Accidents']
print(time_series_accidents_world_rows)

# Create lists to store country names and their corresponding data
countries_list = []
countries_data = []

# Get the country names and data (columns excluding 'Topic')
number_of_countries = len(time_series_accidents_world_rows)
for i in range(len(time_series_accidents_world_rows)):
    country_name = time_series_accidents_world_rows.iloc[i, 1]
    countries_list.append(country_name)
    print(f"Country {i}: {country_name}")
    
    country_data = time_series_accidents_world_rows.iloc[i, 2:].tolist()
    countries_data.append(country_data)
    print(f"Data for {country_name}: {country_data}")

#get the world years and values
time_series_accidents_years_world = time_series_World_data.columns[2:].tolist()  # Exclude both 'Topic' and 'Country' columns

# Get the sources for world data
time_series_accidents_world_sources_rows = time_series_World_data_sources[time_series_World_data_sources['Topic'] == 'Car Accidents']
print(time_series_accidents_world_sources_rows)
# Create lists to store country names and their corresponding data
countries_sources_list = []
countries_sources_data = []

# Get the country names and data (columns excluding 'Topic')
number_of_countries_sources = len(time_series_accidents_world_sources_rows)
for i in range(len(time_series_accidents_world_sources_rows)):
    country_name = time_series_accidents_world_sources_rows.iloc[i, 1]
    countries_sources_list.append(country_name)
    print(f"Country {i}: {country_name}")
    country_data = time_series_accidents_world_sources_rows.iloc[i, 2:].tolist()
    countries_sources_data.append(country_data)
    print(f"Data for {country_name}: {country_data}")
# Path to the JSON file
json_file_path = os.path.join(script_dir, '..', 'website', 'data', 'statistics.json')

# Read existing JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Update the traffic accidents deaths data
json_data['iran_statistics']['statistics']['traffic_accidents_deaths']['deaths']['daily_average'] = last_daily_avg
json_data['iran_statistics']['statistics']['traffic_accidents_deaths']['deaths']['monthly_average'] = last_monthly_avg
json_data['iran_statistics']['statistics']['traffic_accidents_deaths']['deaths']['yearly_average'] = last_yearly_avg
json_data['iran_statistics']['details']['traffic_accidents_deaths']['title'] = accidents_title
json_data['iran_statistics']['details']['traffic_accidents_deaths']['description'] = accidents_description
json_data['iran_statistics']['details']['traffic_accidents_deaths']['sources'] = accidents_sources
json_data['iran_statistics']['details']['traffic_accidents_deaths']['sources_links'] = accidents_sources_links
json_data['iran_statistics']['details']['traffic_accidents_deaths']['chartYears'] = [int(year) for year in time_series_accidents_years]
json_data['iran_statistics']['details']['traffic_accidents_deaths']['chartData'] = time_series_accidents_values 

# Get the world years and values
json_data['iran_statistics']['details']['traffic_accidents_deaths']['world']['chartYears'] = [int(year) for year in time_series_accidents_years_world]

# Initialize the world countries data structure
for i in range(number_of_countries):
    country_name = countries_list[i]
    country_data = countries_data[i]
    
    # Clean and convert data: handle commas, NaN values, and int64 types
    cleaned_data = []
    for value in country_data:
        if pd.notna(value) and str(value).strip() != '':
            # Remove commas and convert to regular Python int
            clean_value = str(value).replace(',', '')
            try:
                cleaned_data.append(int(clean_value))
            except ValueError:
                cleaned_data.append(None)
        else:
            cleaned_data.append(None)
    
    # Create a proper structure for each country
    json_data['iran_statistics']['details']['traffic_accidents_deaths']['world'][country_name] = {
        'chartData': cleaned_data,
        'source' : 'Source',
        'sources_link': countries_sources_data[i] if i < len(countries_sources_data) else []
    }


#End of the Accidents data

# Importing the Air Pollution rows
air_pollution_rows = data[data['Topic'] == 'Air Pollution']
print(air_pollution_rows)
#get the last daily monthly and yearly average (extract first value from Series)
last_daily_avg = int(round(air_pollution_rows['Daily_Average'].iloc[0]))
last_monthly_avg = int(round(air_pollution_rows['Monthly_Average'].iloc[0]))
last_yearly_avg = int(air_pollution_rows['Forecast_Number'].iloc[0])


#get the details of pollution
details_pollution_rows = details_data[details_data['Topic'] == 'Air Pollution']
pollution_title = details_pollution_rows['Title'].iloc[0]
pollution_description = details_pollution_rows['Description'].iloc[0]
pollution_sources = details_pollution_rows['Sources'].iloc[0].split(';')
pollution_sources_links = details_pollution_rows['Sources_Link'].iloc[0].split(';')



#get the time series data for pollution in Iran
time_series_pollution_years = time_series_Iran_data.columns[1:].tolist()  # Exclude the 'Topic' column
time_series_pollution_rows = time_series_Iran_data[time_series_Iran_data['Topic'] == 'Air Pollution']
# Convert to regular Python list with proper int conversion
time_series_pollution_values = [int(val) if pd.notna(val) else None for val in time_series_pollution_rows.iloc[0, 1:].tolist()]
# print(time_series_pollution_values)


# Get the row corresponding to 'Air Pollution' for time series_world_data
time_series_pollution_world_rows = time_series_World_data[time_series_World_data['Topic'] == 'Air Pollution']
print(time_series_pollution_world_rows)

# Create lists to store country names and their corresponding data
countries_list = []
countries_data = []

# Get the country names and data (columns excluding 'Topic')
number_of_countries = len(time_series_pollution_world_rows)
for i in range(len(time_series_pollution_world_rows)):
    country_name = time_series_pollution_world_rows.iloc[i, 1]
    countries_list.append(country_name)
    print(f"Country {i}: {country_name}")
    
    country_data = time_series_pollution_world_rows.iloc[i, 2:].tolist()
    countries_data.append(country_data)
    print(f"Data for {country_name}: {country_data}")

#get the world years and values
time_series_years_world = time_series_World_data.columns[2:].tolist()  # Exclude both 'Topic' and 'Country' columns

# Get the sources for world data
time_series_air_pollution_world_sources_rows = time_series_World_data_sources[time_series_World_data_sources['Topic'] == 'Air Pollution']
print(time_series_air_pollution_world_sources_rows)
# Create lists to store country names and their corresponding data
countries_sources_list = []
countries_sources_data = []

# Get the country names and data (columns excluding 'Topic')
number_of_countries_sources = len(time_series_air_pollution_world_sources_rows)
for i in range(len(time_series_air_pollution_world_sources_rows)):
    country_name = time_series_air_pollution_world_sources_rows.iloc[i, 1]
    countries_sources_list.append(country_name)
    print(f"Country {i}: {country_name}")
    country_data = time_series_air_pollution_world_sources_rows.iloc[i, 2:].tolist()
    countries_sources_data.append(country_data)
    print(f"Data for {country_name}: {country_data}")

# Update the traffic pollution deaths data
json_data['iran_statistics']['statistics']['air_pollution']['deaths']['daily_average'] = last_daily_avg
json_data['iran_statistics']['statistics']['air_pollution']['deaths']['monthly_average'] = last_monthly_avg
json_data['iran_statistics']['statistics']['air_pollution']['deaths']['yearly_average'] = last_yearly_avg
json_data['iran_statistics']['details']['air_pollution_deaths']['title'] = pollution_title
json_data['iran_statistics']['details']['air_pollution_deaths']['description'] = pollution_description
json_data['iran_statistics']['details']['air_pollution_deaths']['sources'] = pollution_sources
json_data['iran_statistics']['details']['air_pollution_deaths']['sources_links'] = pollution_sources_links
json_data['iran_statistics']['details']['air_pollution_deaths']['chartYears'] = [int(year) for year in time_series_pollution_years]
json_data['iran_statistics']['details']['air_pollution_deaths']['chartData'] = time_series_pollution_values


# Get the world years and values
json_data['iran_statistics']['details']['air_pollution_deaths']['world']['chartYears'] = [int(year) for year in time_series_years_world]

# Initialize the world countries data structure
for i in range(number_of_countries):
    country_name = countries_list[i]
    country_data = countries_data[i]
    
    # Clean and convert data: handle commas, NaN values, and int64 types
    cleaned_data = []
    for value in country_data:
        if pd.notna(value) and str(value).strip() != '':
            # Remove commas and convert to regular Python int
            clean_value = str(value).replace(',', '')
            try:
                cleaned_data.append(int(clean_value))
            except ValueError:
                cleaned_data.append(None)
        else:
            cleaned_data.append(None)
    
    # Create a proper structure for each country
    json_data['iran_statistics']['details']['air_pollution_deaths']['world'][country_name] = {
        'chartData': cleaned_data,
        'source' : 'Source',
        'sources_link': countries_sources_data[i] if i < len(countries_sources_data) else []
    }


#End of the Air Pollution data

# Start the education dropout data
education_dropout_rows = data[data['Topic'] == 'Education Dropout']

#get the last daily monthly and yearly average (extract first value from Series)
last_daily_avg = int(round(education_dropout_rows['Daily_Average'].iloc[0]))
last_monthly_avg = int(round(education_dropout_rows['Monthly_Average'].iloc[0]))
last_yearly_avg = int(education_dropout_rows['Forecast_Number'].iloc[0])

#get the details of education dropout
details_education_rows = details_data[details_data['Topic'] == 'Education Dropout']
education_title = details_education_rows['Title'].iloc[0]
education_description = details_education_rows['Description'].iloc[0]
education_sources = details_education_rows['Sources'].iloc[0].split(';')
education_sources_links = details_education_rows['Sources_Link'].iloc[0].split(';')

#get the time series data for education dropout in Iran
time_series_education_years = time_series_Iran_data.columns[1:].tolist()  # Exclude the 'Topic' column
time_series_education_rows = time_series_Iran_data[time_series_Iran_data['Topic'] == 'Education Dropout']
# Convert to regular Python list with proper int conversion
time_series_education_values = [int(val) if pd.notna(val) else None for val in time_series_education_rows.iloc[0, 1:].tolist()]
# print(time_series_education_values)

# Update the traffic education dropout data
json_data['iran_statistics']['statistics']['education']['dropouts']['daily_average'] = last_daily_avg
json_data['iran_statistics']['statistics']['education']['dropouts']['monthly_average'] = last_monthly_avg
json_data['iran_statistics']['statistics']['education']['dropouts']['yearly_average'] = last_yearly_avg
json_data['iran_statistics']['details']['education_dropouts']['title'] = education_title
json_data['iran_statistics']['details']['education_dropouts']['description'] = education_description
json_data['iran_statistics']['details']['education_dropouts']['sources'] = education_sources
json_data['iran_statistics']['details']['education_dropouts']['sources_links'] = education_sources_links
json_data['iran_statistics']['details']['education_dropouts']['chartYears'] = [int(year) for year in time_series_education_years]
json_data['iran_statistics']['details']['education_dropouts']['chartData'] = time_series_education_values

# End of the education dropout data

# Workers data
workers_rows = data[data['Topic'] == 'Workers Died']

#get the last daily monthly and yearly average (extract first value from Series)
last_daily_avg = int(round(workers_rows['Daily_Average'].iloc[0]))
last_monthly_avg = int(round(workers_rows['Monthly_Average'].iloc[0]))
last_yearly_avg = int(workers_rows['Forecast_Number'].iloc[0])

#get the details of workers deaths
details_workers_rows = details_data[details_data['Topic'] == 'Workers Died']
workers_title = details_workers_rows['Title'].iloc[0]
workers_description = details_workers_rows['Description'].iloc[0]
workers_sources = details_workers_rows['Sources'].iloc[0].split(';')
workers_sources_links = details_workers_rows['Sources_Link'].iloc[0].split(';')


#get the time series data for workers deaths in Iran
time_series_workers_years = time_series_Iran_data.columns[1:].tolist()  # Exclude the 'Topic' column
time_series_workers_rows = time_series_Iran_data[time_series_Iran_data['Topic'] == 'Workers Died']
# Convert to regular Python list with proper int conversion
time_series_workers_values = [int(val) if pd.notna(val) else None for val in time_series_workers_rows.iloc[0, 1:].tolist()]
# print(time_series_workers_values)

# Get the row corresponding to 'Air Pollution' for time series_world_data
time_series_workers_world_rows = time_series_World_data[time_series_World_data['Topic'] == 'Workers Died']
print(time_series_workers_world_rows)

# Create lists to store country names and their corresponding data
countries_list = []
countries_data = []

# Get the country names and data (columns excluding 'Topic')
number_of_countries = len(time_series_workers_world_rows)
for i in range(len(time_series_workers_world_rows)):
    country_name = time_series_workers_world_rows.iloc[i, 1]
    countries_list.append(country_name)
    print(f"Country {i}: {country_name}")

    country_data = time_series_workers_world_rows.iloc[i, 2:].tolist()
    countries_data.append(country_data)
    print(f"Data for {country_name}: {country_data}")

#get the world years and values
time_series_years_world = time_series_World_data.columns[2:].tolist()  # Exclude both 'Topic' and 'Country' columns

# Get the sources for world data
time_series_workers_world_sources_rows = time_series_World_data_sources[time_series_World_data_sources['Topic'] == 'Workers Died']
print(time_series_workers_world_sources_rows)
# Create lists to store country names and their corresponding data
countries_sources_list = []
countries_sources_data = []

# Get the country names and data (columns excluding 'Topic')
number_of_countries_sources = len(time_series_workers_world_sources_rows)
for i in range(len(time_series_workers_world_sources_rows)):
    country_name = time_series_workers_world_sources_rows.iloc[i, 1]
    countries_sources_list.append(country_name)
    print(f"Country {i}: {country_name}")
    country_data = time_series_workers_world_sources_rows.iloc[i, 2:].tolist()
    countries_sources_data.append(country_data)
    print(f"Data for {country_name}: {country_data}")





# Update the workers deaths data
json_data['iran_statistics']['statistics']['workers']['deaths']['daily_average'] = last_daily_avg
json_data['iran_statistics']['statistics']['workers']['deaths']['monthly_average'] = last_monthly_avg
json_data['iran_statistics']['statistics']['workers']['deaths']['yearly_average'] = last_yearly_avg
json_data['iran_statistics']['details']['workers_deaths']['title'] = workers_title
json_data['iran_statistics']['details']['workers_deaths']['description'] = workers_description
json_data['iran_statistics']['details']['workers_deaths']['sources'] = workers_sources
json_data['iran_statistics']['details']['workers_deaths']['sources_links'] = workers_sources_links
json_data['iran_statistics']['details']['workers_deaths']['chartYears'] = [int(year) for year in time_series_workers_years]
json_data['iran_statistics']['details']['workers_deaths']['chartData'] = time_series_workers_values


# Get the world years and values
json_data['iran_statistics']['details']['workers_deaths']['world']['chartYears'] = [int(year) for year in time_series_years_world]

# Initialize the world countries data structure
for i in range(number_of_countries):
    country_name = countries_list[i]
    country_data = countries_data[i]
    
    # Clean and convert data: handle commas, NaN values, and int64 types
    cleaned_data = []
    for value in country_data:
        if pd.notna(value) and str(value).strip() != '':
            # Remove commas and convert to regular Python int
            clean_value = str(value).replace(',', '')
            try:
                cleaned_data.append(int(clean_value))
            except ValueError:
                cleaned_data.append(None)
        else:
            cleaned_data.append(None)
    
    # Create a proper structure for each country
    json_data['iran_statistics']['details']['workers_deaths']['world'][country_name] = {
        'chartData': cleaned_data,
        'source' : 'Source',
        'sources_link': countries_sources_data[i] if i < len(countries_sources_data) else []
    }

# End of the workers deaths data

# Death penalty data
death_penalty_rows = data[data['Topic'] == 'Death Penalty']


#get the last daily monthly and yearly average (extract first value from Series)
last_daily_avg = int(round(death_penalty_rows['Daily_Average'].iloc[0]))
last_monthly_avg = int(round(death_penalty_rows['Monthly_Average'].iloc[0]))
last_yearly_avg = int(death_penalty_rows['Forecast_Number'].iloc[0])

#get the details of death penalty
details_death_penalty_rows = details_data[details_data['Topic'] == 'Death Penalty']
death_penalty_title = details_death_penalty_rows['Title'].iloc[0]
death_penalty_description = details_death_penalty_rows['Description'].iloc[0]
death_penalty_sources = details_death_penalty_rows['Sources'].iloc[0].split(';')
death_penalty_sources_links = details_death_penalty_rows['Sources_Link'].iloc[0].split(';')

#get the time series data for death penalty in Iran
time_series_death_penalty_years = time_series_Iran_data.columns[1:].tolist()  # Exclude the 'Topic' column
time_series_death_penalty_rows = time_series_Iran_data[time_series_Iran_data['Topic'] == 'Death Penalty']
# Convert to regular Python list with proper int conversion
time_series_death_penalty_values = [int(val) if pd.notna(val) else None for val in time_series_death_penalty_rows.iloc[0, 1:].tolist()]
# print(time_series_death_penalty_values)

# Update the death penalty data
json_data['iran_statistics']['statistics']['death_penalty']['daily_average'] = last_daily_avg
json_data['iran_statistics']['statistics']['death_penalty']['monthly_average'] = last_monthly_avg
json_data['iran_statistics']['statistics']['death_penalty']['yearly_average'] = last_yearly_avg
json_data['iran_statistics']['details']['death_penalty']['title'] = death_penalty_title
json_data['iran_statistics']['details']['death_penalty']['description'] = death_penalty_description
json_data['iran_statistics']['details']['death_penalty']['sources'] = death_penalty_sources
json_data['iran_statistics']['details']['death_penalty']['sources_links'] = death_penalty_sources_links
json_data['iran_statistics']['details']['death_penalty']['chartYears'] = [int(year) for year in time_series_death_penalty_years]
json_data['iran_statistics']['details']['death_penalty']['chartData'] = time_series_death_penalty_values


# Update the last_updated timestamp
json_data['iran_statistics']['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

# Write the updated data back to JSON file
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)

print(f"Successfully updated JSON file with:")


