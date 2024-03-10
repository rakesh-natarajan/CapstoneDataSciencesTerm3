import pandas as pd
import ssl #you can comment this line
import plotly.subplots
import plotly.graph_objects
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context  #you can comment this line


dat = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
US_data = dat[dat['Country/Region'] == 'US'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
US_data.reset_index(inplace=True)
US_data = pd.melt(US_data, id_vars='index', var_name='Date', value_name='CumulativeDeaths')
US_data['DailyDeaths'] = US_data['CumulativeDeaths'].diff()
US_data['Date'] = pd.to_datetime(US_data['Date'], format='%m/%d/%y')
US_data['Smoothed_deaths'] = US_data['DailyDeaths'].rolling(window=10).mean().astype(float) 
US_data['Smoothed_deaths'] = US_data['Smoothed_deaths'].fillna(0) 
US_deaths = US_data.copy()

dat = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
US_data = dat[dat['Country/Region'] == 'US'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
US_data.reset_index(inplace=True)
US_data = pd.melt(US_data, id_vars='index', var_name='Date', value_name='CumulativeCases')
US_data['DailyCases'] = US_data['CumulativeCases'].diff()
US_data['Date'] = pd.to_datetime(US_data['Date'], format='%m/%d/%y')
US_data['Smoothed_cases'] = US_data['DailyCases'].rolling(window=10).mean().astype(float) 
US_data['Smoothed_cases'] = US_data['Smoothed_cases'].fillna(0) 
US_cases = US_data.copy()

dat = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

US_data = dat[dat['Country/Region'] == 'US'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
US_data.reset_index(inplace=True)
US_data = pd.melt(US_data, id_vars='index', var_name='Date', value_name='CumulativeRecovery')
US_data['DailyRecovery'] = US_data['CumulativeRecovery'].diff()
US_data['Date'] = pd.to_datetime(US_data['Date'], format='%m/%d/%y')
#US_data['Smoothed_recoveries'] = US_data['DailyRecovery'].rolling(window=10).mean
US_recovery = US_data[US_data['Date'] < '2020-12-14'].copy()
US_data = US_deaths.merge(US_recovery, on='Date', how='outer').merge(US_cases, on='Date', how='outer')


#Calculated recoveries = cases on day 14 minus deaths on day 1

# Create a new column 'Calc_recoveries' and set all values to 0
US_data['Calc_recoveries'] = 0

# Calculate 'Calc_recoveries' for rows 14 onwards
US_data.loc[14:, 'Calc_recoveries'] = -US_data.loc[14:, 'Smoothed_deaths'].values + US_data.loc[:len(US_data)-15, 'Smoothed_cases'].values
#still getting a future warning for this, likely need to be cautious with resulting data shape/format

#print(US_data)

fig = plotly.subplots.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1)


fig.add_trace(
    plotly.graph_objects.Scatter(
        x=US_data['Date'], 
        y=US_data['Smoothed_cases'], 
        mode='lines', 
        name='Daily Cases',
        line=dict(color='green')
    ), row=1, col=1
)

fig.add_trace(
    plotly.graph_objects.Scatter(
        x=US_data['Date'], 
        y=US_data['DailyRecovery'],
        #y=US_data['Smoothed_recoveries'], 
        mode='lines', 
        name='Daily Recovery - Reported',
        line=dict(color='blue')
    ), row=2, col=1
)
fig.add_trace(
    plotly.graph_objects.Scatter(
        x=US_data['Date'], 
        y=US_data['Calc_recoveries'],
        #y=US_data['Smoothed_recoveries'], 
        mode='lines', 
        name='Daily Recovery - Estimated',
        line=dict(color='purple')
    ), row=2, col=1
)

fig.add_trace(
    plotly.graph_objects.Scatter(
        x=US_data['Date'], 
        y=US_data['Smoothed_deaths'], 
        mode='lines', 
        name='Daily Deaths',
        line=dict(color='red')
        
    ), row=3, col=1
)

fig.update_yaxes(range=[0, 10000], row=3, col=1)

fig.update_layout(
    title='Daily COVID-19 Recoveries, Cases, and Deaths in the United States <br><sup>Data Source: <a href="https://github.com/CSSEGISandData/COVID-19"> COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University </a> </sup>',
    height=900,
    xaxis=dict( showticklabels=False),
    yaxis=dict(title='Recoveries', showline=False, showgrid=False),  
    yaxis2=dict(title='Cases', showline=False, showgrid=False),  
    yaxis3=dict(title='Deaths', showline=False, showgrid=False),  
    yaxis3_showgrid=True, 
    xaxis3=dict(rangeslider=dict(visible=True, thickness=0.05), type="date")
)

import streamlit as st
# Set the title and a short description
st.title('COVID-19 Dashboard')
st.write(""" 
         Theresa Boyer, Karin Halsey, Rakesh Natarajan, Medha Kaul
         """)

# Display the plot
st.plotly_chart(fig)

st.write(""" 
         All data was smoothed with the 10-day running average to reduce impact of intermittent reporting.

         The reported recoveries were derived based on state-level reporting and was aggregatted by the JHU CSSE COVID-19 respository. Data reporting for recoveries was halted prior to the end of the time series.

         The estimated number of recoveries was derived based on the number of cases - the number of deaths (lagged by 14 days).
         """)

# to run this, type: python3 -m streamlit run RakeshNatarajan/combined.py --theme.base="light" 
