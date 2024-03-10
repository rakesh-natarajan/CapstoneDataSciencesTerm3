import pandas as pd
import ssl #you can comment this line
import plotly.subplots
import plotly.graph_objects

ssl._create_default_https_context = ssl._create_unverified_context  #you can comment this line

dat = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

US_data = dat[dat['Country/Region'] == 'US'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
US_data.reset_index(inplace=True)
US_data = pd.melt(US_data, id_vars='index', var_name='Date', value_name='CumulativeRecovery')
US_data['DailyRecovery'] = US_data['CumulativeRecovery'].diff()
US_data['Date'] = pd.to_datetime(US_data['Date'], format='%m/%d/%y')
US_recovery = US_data[US_data['Date'] < '2020-12-14'].copy()


dat = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
US_data = dat[dat['Country/Region'] == 'US'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
US_data.reset_index(inplace=True)
US_data = pd.melt(US_data, id_vars='index', var_name='Date', value_name='CumulativeDeaths')
US_data['DailyDeaths'] = US_data['CumulativeDeaths'].diff()
US_data['Date'] = pd.to_datetime(US_data['Date'], format='%m/%d/%y')
US_deaths = US_data.copy()

dat = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
US_data = dat[dat['Country/Region'] == 'US'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
US_data.reset_index(inplace=True)
US_data = pd.melt(US_data, id_vars='index', var_name='Date', value_name='CumulativeCases')
US_data['DailyCases'] = US_data['CumulativeCases'].diff()
US_data['Date'] = pd.to_datetime(US_data['Date'], format='%m/%d/%y')
US_cases = US_data.copy()


US_data = US_deaths.merge(US_recovery, on='Date', how='outer').merge(US_cases, on='Date', how='outer')


fig = plotly.subplots.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1)

fig.add_trace(
    plotly.graph_objects.Scatter(
        x=US_data['Date'], 
        y=US_data['DailyRecovery'], 
        mode='lines', 
        name='Daily Recovery',
        line=dict(color='blue')
    ), row=1, col=1
)

fig.add_trace(
    plotly.graph_objects.Scatter(
        x=US_data['Date'], 
        y=US_data['DailyCases'], 
        mode='lines', 
        name='Daily Cases',
        line=dict(color='green')
    ), row=2, col=1
)

fig.add_trace(
    plotly.graph_objects.Scatter(
        x=US_data['Date'], 
        y=US_data['DailyDeaths'], 
        mode='lines', 
        name='Daily Deaths',
        line=dict(color='red')
    ), row=3, col=1
)

fig.update_layout(
    title='Daily COVID-19 Recoveries, Cases, and Deaths in the United States <br><sup>Data Source: <a href="https://github.com/CSSEGISandData/COVID-19"> COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University </a> </sup>',
    height=800,
    xaxis=dict( showticklabels=False),
    yaxis=dict(title='Recoveries', showline=False, showgrid=False),  
    yaxis2=dict(title='Cases', showline=False, showgrid=False),  
    yaxis3=dict(title='Deaths', showline=False, showgrid=False),  
    yaxis3_showgrid=True, 
    xaxis3=dict(rangeslider=dict(visible=True, thickness=0.05), type="date")
)

import streamlit as st
# Set the title and a short description
st.title('COVID-19 dashboard')
# Display the plot
st.plotly_chart(fig)


# to run this, type: python3 -m streamlit run RakeshNatarajan/combined.py