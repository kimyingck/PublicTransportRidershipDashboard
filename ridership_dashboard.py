import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from streamlit_extras.add_vertical_space import add_vertical_space
import plotly.graph_objects as go


# load data
URL_DATA = 'https://storage.data.gov.my/transportation/ridership_headline.parquet'
df = pd.read_parquet(URL_DATA)
if 'date' in df.columns: df['date'] = pd.to_datetime(df['date'])


# State mapping 
state_mapping = {
    "Kuala Lumpur": ["bus_rkl", "rail_lrt_kj", "rail_lrt_ampang", "rail_monorail", 
                     "rail_mrt_kajang", "rail_mrt_pjy"],
    "Penang": ["bus_rpn"],
    "Kuantan": ["bus_rkn"],
    "Cross-State": ["rail_ets", "rail_intercity", "rail_komuter", 
                 "rail_komuter_utara", "rail_tebrau"]
}

# Landing Page
# Create the top section of the page 
st.set_page_config(page_title="Malaysia Public Transport Ridership Dashboard 🚆", layout="wide",initial_sidebar_state="collapsed")
st.title("Welcome to the Public Transport Ridership Dashboard 🚆")
st.subheader("A deep dive into Malaysia's public transport ridership trends from 2019 to 2024.")
st.markdown("""This dashboard presents key trends in public transport ridership based on data from [data.gov.my](https://data.gov.my/).
            Explore interactive visualizations to gain insights into public transport usage across different regions and modes of transportation.""")

# Create optional description section in a expander 
with st.expander("Learn More About This Project 📖"):
    st.markdown("""
    - **Data Source**: The data is sourced from Malaysia's official open data portal, [data.gov.my](https://data.gov.my/).
    - **Purpose**: To analyze and visualize ridership trends to assist in policy-making and resource allocation.
    - **Features**:
        - Interactive charts for rail and bus ridership trends.
        - Correlation heatmaps to reveal relationships between different transportation modes.
        - Insights into seasonal and weekly ridership patterns.
    """)

# Create an expander for variable descriptions
with st.expander("Data Description"):
    st.markdown(
        """
        Below is a list of the key variables in this dataset.\n
        **Note**: All ridership data refers to the number of trips made by the transport system, NOT the number of unique individuals using the service.
        """
    )

    # Define the variable definitions as a dictionary
    variable_definitions = {
        'date (Date)': 'Date in YYYY-MM-DD format',
        'bus_rkl (Integer)': 'Ridership: Rapid Bus (KL)',
        'bus_rkn (Integer)': 'Ridership: Rapid Bus (Kuantan)',
        'bus_rpn (Integer)': 'Ridership: Rapid Bus (Penang)',
        'rail_lrt_ampang (Integer)': 'Ridership: LRT Ampang Line ',
        'rail_lrt_kj (Integer)': 'Ridership: LRT Kelana Jaya Line',
        'rail_monorail (Integer)': 'Ridership: Monorail Line',
        'rail_mrt_kajang (Integer)': 'Ridership: MRT Kajang Line',
        'rail_mrt_pjy (Integer)': 'Ridership: MRT Putrajaya Line',
        'rail_ets (Integer)': 'Ridership: KTMB ETS',
        'rail_komuter (Integer)': 'Ridership: KTM Komuter Utara',
        'rail_tebrau (Integer)': 'Ridership: KTM Shuttle Tebrau',
        'rail_intercity (Integer)': 'Ridership: KTM Intercity'
    }

    # Create a DataFrame for better UI/UX
    new_df = pd.DataFrame(variable_definitions.items(), columns=['Variable', 'Description'])

    # Display the variable descriptions
    st.write("### Variable Descriptions")
    st.table(new_df.style.applymap(lambda x: 'background-color: #f2f2f2' if x else ''))

    # Display the download button for the CSV file
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')
    csv = convert_df(df)
    st.write("You can get the latest data from [data.gov.my](https://data.gov.my/) or you download it here using the button")
    st.download_button(
        "Press to Download",
        csv,
        "ridership_data.csv",
        "text/csv",
        key='download-csv'
    )

st.markdown("<br>", unsafe_allow_html=True)

# Display KPIs
# Function to simplify large numbers for display
def format_number(number):
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(number)
    
# Total Ridership
col1, col2, col3,col4 = st.columns(4)

# KPI 1: Total Ridership 
total_ridership = df[['bus_rkl', 'bus_rkn', 'bus_rpn', 'rail_lrt_ampang', 'rail_mrt_kajang', 
                      'rail_lrt_kj', 'rail_monorail', 'rail_mrt_pjy', 'rail_ets', 'rail_intercity', 
                      'rail_komuter_utara', 'rail_tebrau', 'rail_komuter']].sum().sum()
with col1:
    st.markdown("**Total Ridership:**")
    st.markdown(f"<h3 style='color: #4CAF50;'>{format_number(total_ridership)} trips</h3>", unsafe_allow_html=True)

# KPI 2: Average Ridership per Day
avg_ridership_per_day = df[['bus_rkl', 'bus_rkn', 'bus_rpn', 'rail_lrt_ampang', 'rail_mrt_kajang', 
                            'rail_lrt_kj', 'rail_monorail', 'rail_mrt_pjy', 'rail_ets', 'rail_intercity', 
                            'rail_komuter_utara', 'rail_tebrau', 'rail_komuter']].sum().mean()
with col2:
    st.markdown("**Average Ridership per Day:**")
    st.markdown(f"<h3>{format_number(avg_ridership_per_day)} trips</h3>", unsafe_allow_html=True)

# KPI 3: Growth Rate (Month-over-month growth in ridership)
df['year'] = df['date'].dt.year.astype('Int64')
df['month'] = df['date'].dt.month.astype('Int64')

# Monthly ridership based on grouped year and month 
monthly_ridership_df = df.groupby(['year', 'month'])[['bus_rkl', 'bus_rkn', 'bus_rpn', 'rail_lrt_ampang', 
                                                     'rail_mrt_kajang', 'rail_lrt_kj', 'rail_monorail', 
                                                     'rail_mrt_pjy', 'rail_ets', 'rail_intercity', 
                                                     'rail_komuter_utara', 'rail_tebrau', 'rail_komuter']].sum()

# Calculate month-over-month growth for each transportation mode
monthly_ridership_df['growth_rate'] = monthly_ridership_df.sum(axis=1).pct_change() * 100

# Calculate the latest growth rate (last row's growth rate)
latest_growth_rate = monthly_ridership_df['growth_rate'].iloc[-1]

with col3:
    growth_rate_color = "red" if latest_growth_rate < 0 else "green"
    st.markdown("**Growth Rate:**")
    st.markdown(f"<h3 style='color: {growth_rate_color};'>{latest_growth_rate:.2f}%</h3>", unsafe_allow_html=True)

# KPI 4: Peak Ridership (maximum number of trips recorded per day)
df['sum_ridership'] = df[['bus_rkl', 'bus_rkn', 'bus_rpn', 
                            'rail_lrt_ampang', 'rail_mrt_kajang', 
                            'rail_lrt_kj', 'rail_monorail', 'rail_mrt_pjy', 
                            'rail_ets', 'rail_intercity', 'rail_komuter_utara', 
                            'rail_tebrau', 'rail_komuter']].sum(axis=1)

# Find the peak ridership value and the corresponding date
peak_ridership = df['sum_ridership'].max()  # Maximum value
peak_ridership_date = df[df['sum_ridership']== peak_ridership]['date'].iloc[0]  

with col4:
    st.markdown("**Peak Ridership:**")
    st.markdown(f"<h3>{format_number(peak_ridership)} trips</h3>", unsafe_allow_html=True)
    st.caption(f"Occurred on: {peak_ridership_date.strftime('%B %d, %Y')}")

# Ridership Trends Visualizations
st.header("Overview Ridership Trends")
# Create the tabs for different time periods: Yearly, Monthly, and Day
tab1, tab2, tab3 = st.tabs(["Yearly", "Monthly", "Day of The Week"])

# Yearly Ridership Trends
with tab1:
    st.subheader("Yearly Ridership Trends (2019-2024)")
    # You can use a line chart or bar chart to show trends over the years.
    yearly_df = df.groupby('year')[['bus_rkl', 'bus_rkn', 'bus_rpn', 
                                              'rail_lrt_ampang', 'rail_mrt_kajang', 
                                              'rail_lrt_kj', 'rail_monorail', 
                                              'rail_mrt_pjy', 'rail_ets', 
                                              'rail_intercity', 'rail_komuter_utara', 
                                              'rail_tebrau', 'rail_komuter']].sum()

    yearly_df['total_ridership'] = yearly_df.sum(axis=1)
    # Plot the yearly ridership trends
    fig_yearly = px.line(yearly_df, x=yearly_df.index, 
                         y='total_ridership', 
                         labels={'total_ridership': 'Total Ridership'},
                         line_shape="linear",
                         markers=True,
                         line_dash_sequence=['solid'],
                         color_discrete_sequence=["#1E90FF"])
    st.plotly_chart(fig_yearly)

# Monthly Ridership Trends
# Monthly Average Ridership Trends
with tab2:
    st.subheader("Monthly Average Ridership Trends (2019-2024)")

    # Group by year and month
    monthly_ridership_df = df.groupby(['year', 'month'])[['bus_rkl', 'bus_rkn', 'bus_rpn', 
                                                          'rail_lrt_ampang', 'rail_mrt_kajang', 
                                                          'rail_lrt_kj', 'rail_monorail', 
                                                          'rail_mrt_pjy', 'rail_ets', 
                                                          'rail_intercity', 'rail_komuter_utara', 
                                                          'rail_tebrau', 'rail_komuter']].sum()

    # Calculate total ridership for each month
    monthly_ridership_df['total_ridership'] = monthly_ridership_df.sum(axis=1)
    monthly_day_count = df.groupby(['year', 'month'])['date'].nunique()

    # Calculate the average ridership for each month
    monthly_ridership_df['average_ridership'] = monthly_ridership_df['total_ridership'] / monthly_day_count

    # Reset index to include year and month as columns
    monthly_ridership_df = monthly_ridership_df.reset_index()

    # Plot
    fig_monthly = px.line(monthly_ridership_df, x='month', y='average_ridership', 
                          color='year', 
                          labels={'average_ridership': 'Average Ridership'},
                          line_shape="linear",
                          color_discrete_sequence=px.colors.qualitative.Set2)  
    
    # Customize x-axis to show month names
    fig_monthly.update_xaxes(title='Month', tickmode='array', 
                             tickvals=monthly_ridership_df['month'], 
                             ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    st.plotly_chart(fig_monthly)

# Day-wise Ridership Trends
with tab3:
    st.subheader("Average Ridership by Day of the Week")

    # Group by day of the week
    df['day_of_week'] = df['date'].dt.day_name()

    # Calculate the mean ridership for each day of the week
    days = df.groupby('day_of_week')[['bus_rkl', 'bus_rkn', 'bus_rpn', 
                                      'rail_lrt_ampang', 'rail_mrt_kajang', 
                                      'rail_lrt_kj', 'rail_monorail', 
                                      'rail_mrt_pjy', 'rail_ets', 
                                      'rail_intercity', 'rail_komuter_utara', 
                                      'rail_tebrau', 'rail_komuter']].mean()

    days = days.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    # Calculate the total ridership 
    days['total_ridership'] = days.sum(axis=1)

    # Calculate the bus and rail ridership breakdown 
    days['bus_ridership'] = days[['bus_rkl', 'bus_rkn', 'bus_rpn']].sum(axis=1)
    days['rail_ridership'] = days[['rail_lrt_ampang', 'rail_mrt_kajang', 'rail_lrt_kj', 
                                   'rail_monorail', 'rail_mrt_pjy', 'rail_ets', 
                                   'rail_intercity', 'rail_komuter_utara', 
                                   'rail_tebrau', 'rail_komuter']].sum(axis=1)

    # Plot day of the week ridership trends
    fig_day = px.bar(days, 
                     x=days.index, 
                     y='total_ridership', 
                     labels={'total_ridership': 'Average Ridership'},
                     color='total_ridership',  
                     color_continuous_scale='Blues', 
                     template='plotly_dark',
                     barmode='group', 
                     category_orders={"day_of_week": ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']} 
                    )

    # Pass the custom bus and rail breakdown data 
    fig_day.update_traces(
    customdata=days[['bus_ridership', 'rail_ridership']].values,
    hovertemplate="<b>Day: </b> %{x}<br><b>Total Ridership: </b> %{y:.0f}<br><b>Bus: </b> %{customdata[0]:.0f}<br><b>Rail: </b> %{customdata[1]:.0f}"
    )

    # Display the plot
    st.plotly_chart(fig_day)
    
st.markdown("<br>", unsafe_allow_html=True)        

st.header("In-Depth Ridership Analysis")     
# st.caption("Analyzing patterns, correlations, and growth in public transport usage.")
# Add a subheader to guide the user
st.subheader('Select Rail or Bus Lines to Analyze:')
selected_df = df.drop(columns=['month', 'year','sum_ridership','day_of_week'])

# Create a checkbox to enable select all options
select_all = st.checkbox("Select All Lines", value=True)
multiselect_options = selected_df.columns[1:]

# If "Select All" is checked, select all available lines in the multiselect
if select_all:
    selected_lines = list(multiselect_options)
else:
    selected_lines = st.multiselect(
        'Choose from the available rail or bus lines:',
        options=multiselect_options, 
        default=multiselect_options[:2]  
    )

# Filter the data based on selected lines
if selected_lines:
    filtered_data = selected_df[['date'] + selected_lines]  
else:
    st.warning("No lines selected. Please select at least one rail or bus line.")
    filtered_data = selected_df[['date']]  

# Display filtered data for transparency 
st.write("Filtered Data Preview:", filtered_data.head())

# Visualization 1: Correlation Between Rail and Bus Lines
st.title('Correlation Between Rail and Bus Lines')
if selected_lines:
    # Compute the correlation matrix for selected lines
    correlation_matrix = selected_df[selected_lines].corr()
    
    # Create a heatmap
    fig_corr = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu',
        colorbar=dict(title='Correlation'),
        hoverongaps=False,
        hovertemplate='Correlation: %{z:.2f}<br>X: %{x}<br>Y: %{y}<extra></extra>'))

    # Update layout
    fig_corr.update_layout(
        xaxis_title="Transport Modes",
        yaxis_title="Transport Modes",
        height=600,
        width=800,
    )
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("Visualizations will appear here once you select rail or bus lines.")

# Insights section 
st.markdown("""
    <div style="background-color:#f7f7f7; padding:10px; border-radius:8px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
    <h3>Insights:</h3>
    <ul style="list-style-type: none; padding-left: 0;">
        <li><b>Moderate to Weak Correlation Between Bus and Rail Ridership:</b> The moderate to weak correlation between bus and rail ridership suggests that these modes might cater to different commuter needs or geographic areas. While buses may cover more localized or less accessible routes, rail services likely serve higher-density, long-distance commuters.</li>
        <li><b>Improving Bus and Rail Connections:</b> Enhancing the integration between bus and rail services could improve the commuter experience. Streamlining transfers and creating seamless connections between buses and rail could make it easier for passengers to use both modes during their commute, reducing travel times and increasing overall system efficiency.</li>
    </ul>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

 # Visualization 2: Weekday vs Weekend Ridership
st.title('Weekday vs Weekend Ridership')
if selected_lines:
    # Classify days as Weekday or Weekend
    df['day_of_week'] = df['date'].dt.day_name()
    weekday_df = df[df['day_of_week'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
    weekend_df = df[df['day_of_week'].isin(['Saturday', 'Sunday'])]
    
    # Calculate ridership for weekdays and weekends
    weekday_ridership = weekday_df[selected_lines].sum(axis=0)
    weekend_ridership = weekend_df[selected_lines].sum(axis=0)
    
    # Create a DataFrame for comparison
    comparison_df = pd.DataFrame({'Weekday': weekday_ridership, 'Weekend': weekend_ridership})
    
    # Reshape the DataFrame 
    comparison_df = comparison_df.reset_index()
    comparison_df = comparison_df.rename(columns={'index': 'Transport Mode'})
    comparison_df_melted = comparison_df.melt(id_vars=['Transport Mode'], value_vars=['Weekday', 'Weekend'], var_name='DayType', value_name='Ridership')
    
    # Create a Plotly bar chart with tooltips
    fig = px.bar(
        comparison_df_melted,
        x='Transport Mode',
        y='Ridership',
        color='DayType',
        color_discrete_map={'Weekday': '#004c8c', 'Weekend': '#eb6060'},
        labels={'Ridership': 'Ridership', 'Transport Mode': 'Transport Mode'},
        hover_data={'Transport Mode': True, 'Ridership': True, 'DayType': True}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Visualizations will appear here once you select rail or bus lines.")

# Insights section
st.markdown("""
    <div style="background-color:#f7f7f7; padding:10px; border-radius:8px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
    <h3>Insights:</h3>
    <ul style="list-style-type: none; padding-left: 0;">
        <li><b>Weekday vs Weekend Ridership:</b> The analysis shows that weekday ridership is consistently higher across all transport modes compared to weekends, particularly during rush hours. This suggests that public transport is mainly used for commuting purposes during weekdays, with higher demand during peak morning and evening hours.</li>
        <li><b>Potential for Adjusting Service Frequencies:</b> The difference in ridership between weekdays and weekends signals an opportunity to adjust service frequencies based on demand. For example, reducing the frequency of buses and rail services during weekends while maintaining high frequencies on weekdays could help reduce operational costs while ensuring service quality is maintained during peak hours.</li>
    </ul>
    </div>
""", unsafe_allow_html=True)

# Visualisation 3: Monthly Comparison of Average Ridership Across Transport Modes
st.title("Monthly Comparison of Average Ridership Across Transport Modes")
if selected_lines:
    # Separate the transport modes 
    bus_columns = ['bus_rkl', 'bus_rkn', 'bus_rpn']
    lrt_columns = ['rail_lrt_ampang', 'rail_lrt_kj']
    mrt_columns = ['rail_mrt_kajang', 'rail_mrt_pjy']
    monorail_columns = ['rail_monorail']
    ets_columns = ['rail_ets']
    intercity_columns = ['rail_intercity']
    komuter_columns = ['rail_komuter_utara', 'rail_komuter', 'rail_tebrau']

    # Group by month and calculate the sum 
    bus_ridership = df.groupby(['month'])[bus_columns].sum()
    lrt_ridership = df.groupby(['month'])[lrt_columns].sum()
    mrt_ridership = df.groupby(['month'])[mrt_columns].sum()
    monorail_ridership = df.groupby(['month'])[monorail_columns].sum()
    ets_ridership = df.groupby(['month'])[ets_columns].sum()
    intercity_ridership = df.groupby(['month'])[intercity_columns].sum()
    komuter_ridership = df.groupby(['month'])[komuter_columns].sum()

    # Calculate the average ridership for each mode across all years
    average_bus_ridership = bus_ridership.sum(axis=1)/len(df['year'].unique())
    average_lrt_ridership = lrt_ridership.sum(axis=1)/len(df['year'].unique())
    average_mrt_ridership = mrt_ridership.sum(axis=1)/len(df['year'].unique())
    average_monorail_ridership = monorail_ridership.sum(axis=1)/len(df['year'].unique())
    average_ets_ridership = ets_ridership.sum(axis=1)/len(df['year'].unique())
    average_intercity_ridership = intercity_ridership.sum(axis=1)/len(df['year'].unique())
    average_komuter_ridership = komuter_ridership.sum(axis=1)/len(df['year'].unique())
    
    # Combine all ridership data 
    ridership_comparison = pd.DataFrame({
        'month': bus_ridership.index,
        'Bus': average_bus_ridership,
        'LRT': average_lrt_ridership,
        'MRT': average_mrt_ridership,
        'Monorial': average_monorail_ridership,
        'ETS': average_ets_ridership,
        'Intercity': average_intercity_ridership,
        'Komuter': average_komuter_ridership
    })

   # A bar chart to compare the average ridership for different transport modes over time
    fig_bar = px.bar(ridership_comparison, 
                     x='month', 
                     y=['Bus', 'LRT', 'MRT',
                        'Monorial', 'ETS', 'Intercity', 
                        'Komuter'],
                     labels={'value': 'Average Ridership', 'month': 'Month'},
                      color_discrete_sequence=px.colors.qualitative.Set1)

    # Chart Layout
    fig_bar.update_layout(
        barmode='stack',  
        xaxis_title="Month",
        yaxis_title="Ridership",
        height=600,
        width=900
    )

    # Update
    fig_bar.update_xaxes(tickmode='array',
                         tickvals=ridership_comparison.index,
                         ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    # Plot the stacked bar chart
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("Visualizations will appear here once you select rail or bus lines.")

st.markdown("""
    <div style="background-color:#f7f7f7; padding:10px; border-radius:8px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
    <h3>Insights:</h3>
    <ul style="list-style-type: none; padding-left: 0;">
        <li><b>Rail vs. Bus Ridership:</b>
            <ul style="list-style-type: none; padding-left: 0;">
                <li><b>Higher Ridership for Rail Modes (LRT, MRT):</b> Rail modes like LRT and MRT consistently show higher ridership compared to buses, suggesting a preference for rail due to its faster travel times, higher frequency, and direct routes in urban areas.</li>
                <li><b>Bus Ridership vs Rail:</b> Although buses are crucial for connecting areas not served by rail, they generally show lower ridership. This could be due to longer travel times, lower frequency, and less predictable schedules compared to rail.</li>
            </ul>
        </li>
        <li><b>Monthly Ridership Trends:</b>
            <ul style="list-style-type: none; padding-left: 0;">
                <li><b>December Peak:</b> December sees the highest ridership across all transport modes, likely driven by year-end holidays and school vacations, when travel demand is higher.</li>
                <li><b>April Low:</b> April shows the lowest ridership, which may be due to fewer holidays and a lull in travel demand compared to other months.</li>
            </ul>
        </li>
        <li><b>Mode Performance Across Months:</b>
            <ul style="list-style-type: none; padding-left: 0;">
                <li><b>LRT Leading:</b> LRT consistently leads in ridership across all months, indicating its high demand in urban areas.</li>
                <li><b>KTM Intercity Low:</b> KTM Intercity consistently records the lowest ridership, reflecting its more regional focus compared to urban-centric modes like LRT and MRT.</li>
            </ul>
        </li>
    </ul>
    </div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)     

# Visualisation 4: Yearly Comparison of Average Ridership Across Transport Modes
st.title("Yearly Comparison of Average Ridership Across Transport Modes")
if selected_lines:
    # Group by year and calculate the sum for each transport mode
    bus_ridership_yearly = df.groupby(['year'])[bus_columns].sum()
    lrt_ridership_yearly = df.groupby(['year'])[lrt_columns].sum()
    mrt_ridership_yearly = df.groupby(['year'])[mrt_columns].sum()
    monorail_ridership_yearly = df.groupby(['year'])[monorail_columns].sum()
    ets_ridership_yearly = df.groupby(['year'])[ets_columns].sum()
    intercity_ridership_yearly = df.groupby(['year'])[intercity_columns].sum()
    komuter_ridership_yearly = df.groupby(['year'])[komuter_columns].sum()

    # Calculate the average ridership for each mode across all months in each year
    average_bus_ridership_yearly = bus_ridership_yearly.sum(axis=1)/12
    average_lrt_ridership_yearly = lrt_ridership_yearly.sum(axis=1)/12
    average_mrt_ridership_yearly = mrt_ridership_yearly.sum(axis=1)/12
    average_monorail_ridership_yearly = monorail_ridership_yearly.sum(axis=1)/12
    average_ets_ridership_yearly = ets_ridership_yearly.sum(axis=1)/12
    average_intercity_ridership_yearly = intercity_ridership_yearly.sum(axis=1)/12
    average_komuter_ridership_yearly = komuter_ridership_yearly.sum(axis=1)/12
    
    # Combine all yearly ridership data
    ridership_comparison_yearly = pd.DataFrame({
        'year': bus_ridership_yearly.index,
        'Bus': average_bus_ridership_yearly,
        'LRT': average_lrt_ridership_yearly,
        'MRT': average_mrt_ridership_yearly,
        'Monorial': average_monorail_ridership_yearly,
        'ETS': average_ets_ridership_yearly,
        'Intercity': average_intercity_ridership_yearly,
        'Komuter': average_komuter_ridership_yearly
    })

    # A bar chart to compare the average ridership for different transport modes across years
    fig_bar_yearly = px.bar(ridership_comparison_yearly, 
                            x='year', 
                            y=['Bus', 'LRT', 'MRT',
                               'Monorial', 'ETS', 'Intercity', 
                               'Komuter'],
                            labels={'value': 'Average Ridership', 'year': 'Year'},
                            color_discrete_sequence=px.colors.qualitative.Set1)

    # Chart Layout for yearly comparison
    fig_bar_yearly.update_layout(
        barmode='group',  
        xaxis_title="Year",
        yaxis_title="Ridership",
        height=600,
        width=900
    )

    # Plot the grouped bar chart
    st.plotly_chart(fig_bar_yearly, use_container_width=True)
else:
    st.info("Visualizations will appear here once you select rail or bus lines.")

# Insights
st.markdown("""
    <div style="background-color:#f7f7f7; padding:10px; border-radius:8px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
    <h3>Insights:</h3>
    
    <!-- Trends Over Time -->
    <h4>Trends Over Time:</h4>
    <ul style="list-style-type: none; padding-left: 0;">
        <li><b>Drastic Decline from 2019 to 2020:</b> A significant decrease in ridership is observed across all transport modes in 2020, primarily due to the COVID-19 pandemic, which led to lockdowns and reduced demand for public transportation.</li>
        <li><b>Continued Decline from 2020 to 2021:</b> Despite the easing of restrictions, ridership remained subdued in 2021, as people were still hesitant to travel and public transport services were limited.</li>
        <li><b>Recovery in 2022:</b> Ridership saw a significant rebound in 2022, following the lifting of travel restrictions and the reopening of the country, leading to increased commuting and regional travel.</li>
        <li><b>Year-on-Year Growth from 2022 to 2024:</b> Ridership continued to grow steadily in 2023 and 2024, driven by the gradual recovery of the economy, improved confidence in public transport, and the continued expansion of rail networks like MRT and LRT.</li>
    </ul>

    <!-- Transport Mode Performance -->
    <h4>Transport Mode Performance:</h4>
    <ul style="list-style-type: none; padding-left: 0;">
        <li><b>LRT:</b> Leads in ridership, with approximately 659.17M passengers.</li>
        <li><b>MRT:</b> Ranked second, but has the highest bounce rate of 37.5%.</li>
        <li><b>KTM Intercity:</b> Records the lowest ridership among the rail services.</li>
        <li><b>Rapid Bus (Kuantan):</b> Shows the lowest ridership among bus services.</li>
    </ul>
    
    </div>
""", unsafe_allow_html=True)

