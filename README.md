# Real-Time Events Counter

## Overview

News reports often cite casualty statistics as abstract numbers, making it difficult to comprehend their true scale and human impact. This project transforms annual mortality data into real-time counters, providing a more tangible understanding of how frequently tragic events occur.

## About This Project

This visualization tool converts yearly statistics into live counters, allowing users to observe the frequency of specific events as they would occur in real-time. By breaking down annual figures into seconds, minutes, and hours, the project aims to make abstract statistics more relatable and impactful.


## Data Sources

Obtaining accurate and up-to-date statistics in Iran presents unique challenges:

- No centralized database exists for many events
- Data sources vary between years and organizations
- Official statistics are typically released annually with significant delays

To address these challenges, data has been compiled through:
- Cross-referencing multiple news sources and official reports
- Validating figures across different publications
- Consulting available government and NGO statistics

All data sources are documented in the respective event folders.

## Methodology

### Forecasting Approach

Since official statistics are released annually, current-year projections are generated using time series forecasting methods. Each event type employs a tailored forecasting approach based on:

- Available historical data points
- Data frequency and reliability
- Observed trends and patterns

Detailed methodology documentation is available in each event-specific folder. **Suggestions for improved forecasting methods are welcome—please open an issue to discuss.**

## Important Notes

### Version 1.0 Limitations

- **Raw Numbers Only**: This version displays absolute figures without normalization or per-capita adjustments to preserve the direct human impact of the statistics
- **Limited Comparability**: International comparisons may not be directly comparable due to population differences and varying data collection methods
- Future versions will include normalized, per-capita metrics for meaningful cross-country comparisons

## Roadmap

- [ ] English language version
- [ ] Normalized/per-capita comparison graphs
- [ ] Additional event types
- [ ] Interactive data visualization enhancements

## Contributing

Contributions are welcome! Areas where help is particularly valuable:

- Identifying more reliable data sources
- Improving forecasting models
- Translation and localization
- Data validation and verification

Please open an issue to discuss proposed changes before submitting a pull request.



---

**Note**: This project aims to honor those affected by these statistics by making their scale more comprehensible. All data is presented with respect for the human lives represented.
