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
    df = pd.read_csv('Dataset_COVID_complete.csv', index_col = [0])
    return df

'##  Global COVID Cases'
df = load_data()


# A Sidebar for choosing different functions
st.sidebar.subheader("Choices of the Dates")
year_2020 = st.sidebar.checkbox('2020')
year_2021 = st.sidebar.checkbox('2021')
month = st.sidebar.slider('Month',1,12,6)
country_choice = "".join(st.sidebar.multiselect("Choose countries", ['France','US','India', 'Brazil', 'South Africa']))
if not country_choice:
    st.sidebar.error("Please select at least one country.")
dt_choice = "".join(st.sidebar.multiselect("Choose Category", ['confirmed','death','recovered']))
if not dt_choice:
    st.sidebar.error("Please select at least one category.")

# Data Viz
if year_2020:
    dfs = df[(df['year'] == 2020 ) & (df['month'] == month)]
    df.loc[(df['month'] == month) &(df['year'] == 2020), df.columns.str.contains(country_choice + "|month|year")]
    fig = px.line(dfs, x= 'Date', y= 'Daily_' + country_choice +'_' + dt_choice )#'Daily_France_death')
    st.plotly_chart(fig)

if year_2021:
    if month > datetime.now().month:
        st.write("Future Dates")
    else:
        dfs = df[(df['year'] == 2021) & (df['month'] == month)]
        df.loc[(df['month'] == month) & (df['year'] == 2021), df.columns.str.contains(country_choice + "|month|year")]
        fig = px.line(dfs, x='Date', y='Daily_' + country_choice + '_' + dt_choice)  # 'Daily_France_death')
        st.plotly_chart(fig)

