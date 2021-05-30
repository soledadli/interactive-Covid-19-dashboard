import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Setting Dashboard Interface


st.title('COVID-19 Dashboard')
st.markdown(
'''A collaborative work of creating an interactive Covid-19 dashboard by Digital Science M1 students from
for Research and Interdisciplinarity. 
[GitHub Project](https://github.com/soledadli/interactive-Covid-19-dashboard)
''')



# Experimenting with Data
@st.cache
def load_data( ):
    df_cases = pd.read_csv('Data_processed/Dataset_COVID_confiremed_complete.csv', index_col = [0])
    df_death= pd.read_csv('Data_processed/Dataset_COVID_Death_complete.csv', index_col=[0])
    df_recovered= pd.read_csv('Data_processed/Dataset_COVID_recovered_complete.csv', index_col=[0])
    return df_cases,df_death,df_recovered

'##  Global COVID Cases'
df_cases,df_death,df_recovered = load_data()
country_choice = []
def df_selection(list_countries_temp, type,df_cases,df_death,df_recovered):
    list_countries_temp[0].append('Date')
    columns_to_filter = list_countries_temp[0]
    if (type =='death'):
        print('death')
        return df_death[columns_to_filter]
    elif (type == 'recovered'):
        print('recovered')
        return df_recovered[columns_to_filter]
    elif (type == 'confirmed'):
        print('confirmed')
        return df_cases[columns_to_filter]

def vis(filter_data,list_countries):
    print(filter_data)
    if (len(list_countries[0])<3):
        fig = px.line(filter_data, x='Date', y=list_countries[0][0])  # 'Daily_France_death')

        return fig
    elif (len(list_countries[0])>2):
        fig = px.line(filter_data, x='Date', y=filter_data.columns[0:-1])
        return fig


# A Sidebar for choosing different functions
st.sidebar.subheader("Choices of the Dates")
year_2020 = st.sidebar.checkbox('2020')
year_2021 = st.sidebar.checkbox('2021')
month = st.sidebar.slider('Month',1,12,6)
country_choice.append(st.sidebar.multiselect("Choose countries", list(df_cases.columns[0:-3]), default='US'))
dt_choice = "".join(st.sidebar.multiselect("Choose Category", ['confirmed','death','recovered'],default = 'confirmed'))

if not country_choice:
    st.sidebar.error("Please select at least one country.")
    #country_choice.append('US')
if not dt_choice:
    st.sidebar.error("Please select at least one category.")
    #dt_choice = 'confirmed'

# Data Viz


data_to_plot = df_selection(country_choice, dt_choice,df_cases,df_death,df_recovered)

fig = vis(data_to_plot,country_choice)
st.plotly_chart(fig)

#if year_2020:
#    dfs = df_cases[(df_cases['year'] == 2020 ) & (df_cases['month'] == month)]
#    df_cases.loc[(df_cases['month'] == month) &(df_cases['year'] == 2020), df_cases.columns.str.contains(country_choice + "|month|year")]
#    fig = px.line(dfs, x= 'Date', y=  country_choice )#'Daily_France_death')
#    st.plotly_chart(fig)

#if year_2021:
#    if month > datetime.now().month:
#        st.write("Future Dates")
#    else:
#        dfs = df_cases[(df_cases['year'] == 2021) & (df_cases['month'] == month)]
#        df_cases.loc[(df_cases['month'] == month) & (df_cases['year'] == 2021), df_cases.columns.str.contains(country_choice + "|month|year")]
#        fig = px.line(dfs, x='Date', y= country_choice )  # 'Daily_France_death')
#        st.plotly_chart(fig)
#'''
