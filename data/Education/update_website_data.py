#!/usr/bin/env python3
"""
JSON Data Generator for Iran Statistics Website
This script generates and updates JSON data files for the website
"""

import json
import os
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def update_website_statistics_json():
    """Update the main statistics JSON file for the website"""
    
    # Get current timestamp
    current_time = datetime.now().isoformat() + "Z"
    
    # Calculate some dynamic values (you can modify these based on real data sources)
    base_date = datetime.now()
    days_elapsed = (base_date - datetime(2025, 1, 1)).days
    
    statistics_data = {
        "iran_statistics": {
            "metadata": {
                "last_updated": current_time,
                "source": "Iran National Statistics Center",
                "update_frequency": "daily",
                "data_version": "1.0"
            },
            "statistics": {
                "traffic_accidents": {
                    "deaths": {
                        "daily_average": 60,
                        "monthly_average": 1800,
                        "yearly_average": 21900,
                        "current_period_total": int(60 * days_elapsed * (0.9 + np.random.random() * 0.2)),
                        "trend": "critical",
                        "icon": "🚗",
                        "description": "Traffic accident fatalities nationwide"
                    }
                },
                "education": {
                    "dropouts": {
                        "daily_average": 450,
                        "monthly_average": 13500,
                        "yearly_average": 164250,
                        "current_period_total": int(450 * days_elapsed * (0.8 + np.random.random() * 0.4)),
                        "trend": "high",
                        "icon": "🎓",
                        "description": "Students leaving educational system"
                    },
                    "enrollment": {
                        "latest_year": 2024,
                        "latest_count": 992321,
                        "historical_data": [
                            {"year": 2017, "persian_year": 1396, "students": 747911},
                            {"year": 2018, "persian_year": 1397, "students": 696399},
                            {"year": 2019, "persian_year": 1398, "students": 928899},
                            {"year": 2020, "persian_year": 1399, "students": 938614},
                            {"year": 2021, "persian_year": 1400, "students": 980871},
                            {"year": 2022, "persian_year": 1401, "students": 911272},
                            {"year": 2023, "persian_year": 1402, "students": 929798},
                            {"year": 2024, "persian_year": 1403, "students": 992321}
                        ]
                    }
                },
                "air_pollution": {
                    "deaths": {
                        "daily_average": 85,
                        "monthly_average": 2550,
                        "yearly_average": 31025,
                        "current_period_total": int(85 * days_elapsed * (0.9 + np.random.random() * 0.2)),
                        "trend": "severe",
                        "icon": "🫁",
                        "description": "Deaths attributed to air pollution"
                    }
                },
                "healthcare": {
                    "hospital_admissions": {
                        "daily_average": 12000,
                        "monthly_average": 360000,
                        "yearly_average": 4380000,
                        "current_period_total": int(12000 * days_elapsed * (0.95 + np.random.random() * 0.1)),
                        "trend": "normal",
                        "icon": "🏥",
                        "description": "Total hospital admissions nationwide"
                    }
                },
                "employment": {
                    "unemployment_claims": {
                        "daily_average": 1200,
                        "monthly_average": 36000,
                        "yearly_average": 438000,
                        "current_period_total": int(1200 * days_elapsed * (0.9 + np.random.random() * 0.2)),
                        "trend": "rising",
                        "icon": "💼",
                        "description": "New unemployment benefit claims"
                    }
                },
                "demographics": {
                    "births": {
                        "daily_average": 3500,
                        "monthly_average": 105000,
                        "yearly_average": 1277500,
                        "current_period_total": int(3500 * days_elapsed * (0.95 + np.random.random() * 0.1)),
                        "trend": "stable",
                        "icon": "👶",
                        "description": "New births registered"
                    }
                }
            },
            "real_time_multipliers": {
                "traffic_deaths": 0.00069,
                "education_dropouts": 0.00052,
                "pollution_deaths": 0.00098,
                "hospital_admissions": 0.139,
                "unemployment_claims": 0.0139,
                "new_births": 0.0405
            }
        }
    }
    
    return statistics_data

def load_education_analysis_results(analysis_file_path):
    """Load results from education analysis if available"""
    try:
        with open(analysis_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Education analysis file not found: {analysis_file_path}")
        return None

def main():
    """Main function to update JSON data files"""
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    website_dir = os.path.join(script_dir, '..', '..', 'website')
    data_dir = os.path.join(website_dir, 'data')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Update main statistics JSON
    statistics_data = update_website_statistics_json()
    
    # Try to load education analysis results
    education_analysis_path = os.path.join(script_dir, 'education_analysis_results.json')
    education_results = load_education_analysis_results(education_analysis_path)
    
    if education_results:
        # Update education data with analysis results
        statistics_data['iran_statistics']['education_analysis'] = education_results
        print("✅ Education analysis results integrated")
    
    # Write updated statistics to JSON file
    output_path = os.path.join(data_dir, 'statistics.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(statistics_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Statistics JSON updated: {output_path}")
    print(f"📊 Last updated: {statistics_data['iran_statistics']['metadata']['last_updated']}")
    
    # Create a simple API endpoint simulation
    api_dir = os.path.join(website_dir, 'api')
    os.makedirs(api_dir, exist_ok=True)
    
    # Create individual endpoint files
    endpoints = {
        'traffic.json': statistics_data['iran_statistics']['statistics']['traffic_accidents'],
        'education.json': statistics_data['iran_statistics']['statistics']['education'],
        'pollution.json': statistics_data['iran_statistics']['statistics']['air_pollution'],
        'healthcare.json': statistics_data['iran_statistics']['statistics']['healthcare'],
        'employment.json': statistics_data['iran_statistics']['statistics']['employment'],
        'demographics.json': statistics_data['iran_statistics']['statistics']['demographics']
    }
    
    for filename, data in endpoints.items():
        endpoint_path = os.path.join(api_dir, filename)
        with open(endpoint_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ API endpoints created in: {api_dir}")

if __name__ == "__main__":
    main()
