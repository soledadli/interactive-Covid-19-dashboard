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
country_choice = st.multiselect("Choose countries", ['France','US','India', 'Brazil', 'South Africa'])
if not country_choice:
    st.error("Please select at least one country.")



# Experimenting with Data
@st.cache
def load_data( ):
    df = pd.read_csv('Dataset_COVID_complete.csv', index_col = [0])
    return df

'##  Global COVID Cases (Confirmed, Recovered and Deaths)'
df = load_data()

#  A sidebar Time slider for changing different dates
st.sidebar.subheader("Choices of the Dates")
year_2020 = st.sidebar.checkbox('2020')
year_2021 = st.sidebar.checkbox('2021')
month = st.sidebar.slider('Month',1,12,6)
if year_2020:
    df[(df['year'] == 2020 ) & (df['month'] == month)]
if year_2021:
    if month > 5:
        st.write("Future Dates")
    else:
        df[(df['year'] == 2021) & (df['month'] == month)]




