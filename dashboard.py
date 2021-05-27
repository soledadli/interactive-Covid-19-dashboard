import streamlit as st
import pandas as pd

df = pd.read_csv('time_series_covid19_recovered_global.csv')
st.title('COVID-19 Dashboard')
countries = st.multiselect("Choose countries", ['France','US','India', 'Brazil', 'South Africa'])
if not countries:
    st.error("Please select at least one country.")