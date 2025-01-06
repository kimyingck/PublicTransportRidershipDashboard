# Public Transport Ridership Dashboard

## Project Overview
The aim of this project is to find patterns, trends, and insights through analysing and visualising data on public transportation ridership. The dataset contains ridership statistics from Malaysia for the period 2019–2024, covering both bus and train services. This project's main objectives are to give users and transportation professionals a thorough grasp of ridership trends, support data-driven decision-making, and help them comprehend usage trends.

## Table of Contents
- [Project Overview](#project-overview)
- [Data Description](#data-description)
- [Analysis & Insights](#analysis--insights)
- [Getting Started](#getting-started)

## Data Description
The dataset contains daily ridership data for various transport modes, with the following columns:
- **Date**: Date of ridership data collection
- **Bus Modes**:
  - `bus_rkl`: Rapid Bus (KL)
  - `bus_rkn`: Rapid Bus (Kuantan)
  - `bus_rpn`: Rapid Bus (Penang)
- **Rail Modes**:
  - `rail_lrt_ampang`: LRT Ampang Line
  - `rail_mrt_kajang`: MRT Kajang
  - `rail_lrt_kj`: LRT Kelana Jaya
  - `rail_monorail`: Monorail
  - `rail_mrt_pjy`:  MRT Putrajaya
  - `rail_ets`: ETS
  - `rail_intercity`: Intercity Rail
  - `rail_komuter_utara`: KTM Komuter Utara
  - `rail_tebrau`:  KTM Shuttle Tebrau
  - `rail_komuter`: KTM Komuter
 
## Analysis & Insights
The project includes several interactive visualizations, including:
1. **Overview Charts**: Total ridership trends by year, month, and day of the week.
2. **Time-based Charts**:
   - **Yearly Ridership**: A line chart showing the overall ridership across years.
   - **Monthly Average Ridership**: Line charts that display average ridership by month, broken down by year.
   - **Day-wise Ridership**: Bar charts that highlight average ridership by the day of the week.
3. **Comparative Charts**:
   - Comparison between **bus** and **rail** ridership with breakdowns by month, year, and mode.
4. **Growth Analysis**: Visual representation of growth in ridership, particularly focusing on rail usage over the years.

## Getting Started
To run the project locally, follow these steps:


1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/PublicTransportRidershipDashboard.git
   cd PublicTransportRidershipDashboard
2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
