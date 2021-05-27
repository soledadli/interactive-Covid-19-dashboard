import streamlit as st
import pandas as pd

# Setting Dashboard Interface
st.title('COVID-19 Dashboard')
st.markdown(
'''A collaborative work of creating an interactive Covid-19 dashboard by Digital Science M1 students from
for Research and Interdisciplinarity. 
[GitHub Project](https://github.com/soledadli/interactive-Covid-19-dashboard)
''')
# Multiselect bar for countries
countries = st.multiselect("Choose countries", ['France','US','India', 'Brazil', 'South Africa'])
#  A sidebar Time slider for changing different dates
date = st.sidebar.slider('Date',1,31,15)
if not countries:
    st.error("Please select at least one country.")

# Experimenting with Data
@st.cache
def test_data(filename):
    df = pd.read_csv('time_series_covid19_'+ filename + '.csv')
    countries = ['France', 'US', 'India', 'Brazil', 'South Africa']
    df = df[df["Country/Region"].isin(countries)].groupby('Country/Region').sum()
    df.rename(columns = {'Lat':'lat','Long':'lon'}, inplace = True)
    return df

'## Recovered_Global Dataframe with selected countries'
recovered = test_data('recovered_global')
recovered
if st.checkbox('Show Deaths Global Data'):
    '### Geo Recovered Data with selected countries'
    st.map(recovered)

'## Deaths_Global Dataframe with selected countries'
death = test_data('deaths_global')
death

