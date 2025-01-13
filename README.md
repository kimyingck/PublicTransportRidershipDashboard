# Public Transport Ridership Dashboard

## Project Overview
The **Public Transport Ridership Dashboard** analyzes and visualizes public transportation ridership data from **2019** to **2024** in Malaysia. The dataset encompasses daily statistics for both **bus** and **train** services. This project aims to uncover ridership patterns, trends, and insights that help both transportation professionals and users understand how various public transport modes are utilized. The insights generated from the analysis support data-driven decision-making and offer a comprehensive understanding of ridership trends over time. The data is sourced from [data.gov.my](https://data.gov.my/data-catalogue/ridership_headline), which provides access to public sector information in Malaysia. The Streamlit Web App can be accessed [here](https://ridership-dashboard.streamlit.app/).



## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Summary of Insights](#summary-of-insights)
   - [Transport Modes Breakdown](#transport-modes-breakdown)
   - [Time-Based Insights](#time-based-insights)
3. [Recommendations](#recommendations)
4. [Getting Started](#getting-started)

## Executive Summary
The analysis indicates that LRT and MRT services consistently record the highest ridership compared to other public transport modes, including buses, monorail, ETS, and KTM. Ridership levels are notably higher on weekdays, with Fridays experiencing the most pronounced increases. Between 2019 and 2021, however, there was a significant decline in ridership, primarily attributed to the disruptions caused by the COVID-19 pandemic, which led to nationwide lockdowns and a substantial reduction in the demand for public transportation services.

## Summary of Insights  

### Transport Modes Breakdown
- **LRT**: Leads in ridership, with approximately **659.17M** passengers.
- **MRT**: Ranked second, but has the highest bounce rate of **37.5%**.
- **KTM Intercity**: Records the lowest ridership among the rail services.
- **Rapid Bus (Kuantan)**: Shows the lowest ridership among bus services.

### Time-Based Insights
- **Weekday Ridership**: Public transport usage peaks on weekdays, with **Fridays** seeing the highest ridership.
- **Decline in 2020-2021**: Ridership significantly decreased from **2020 to 2021**, correlating with the **COVID-19 pandemic**, which caused lockdowns and reduced demand.
- **Recovery in 2022**: After the reopening of the country and the lifting of travel restrictions, ridership sharply rebounded in **2022**, reflecting an uptick in commuting and travel.

## Recommendations

### 1. Prioritize Weekday Campaigns  
The notable difference in ridership between weekdays and weekends suggests a need for optimized service scheduling. Reducing service frequencies on weekends while maintaining high frequencies on weekdays could optimize operations, reduce costs, and ensure high-quality service during peak hours.

### 2. Enhance Rail Infrastructure & Integration  
Expanding the rail network and improving connections with bus services could create a more efficient and seamless travel experience for commuters. A well-integrated transport system will enable smooth transitions between modes of transport, improving convenience and overall system efficiency.

## Getting Started
To run the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/PublicTransportRidershipDashboard.git
   cd PublicTransportRidershipDashboard

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
