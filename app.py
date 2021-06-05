import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Setting Dashboard Interface


st.title('COVID-19 Dashboard')
st.markdown(
'''A collaborative work of creating an interactive Covid-19 dashboard by [Digital Science] (https://master.cri-paris.org/en/digital) M1 students from
for Research and Interdisciplinarity. 
[GitHub Project](https://github.com/soledadli/interactive-Covid-19-dashboard)

Data source: [COVID-19 Data Repository](https://github.com/CSSEGISandData/COVID-19) by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University

## How to use this dashboard?

First, choose the period to analyze between two dates to select from a calendar.
Second, the user can choose to view a single country or compare two or more countries between countries.
Third, select the template type on the chart.
Fourth, choose from three types of statistics, confirmed deaths, confirmed cases, and recovered people.
Finally, to compare two or more countries in absolute numbers, it is better to use the option "Non-normalized data",
but to compare two or more countries with significant differences in population, the best option is "Normalized over 100k".
''')


# Experimenting with Data
@st.cache
def load_data( ):
    df_cases = pd.read_csv('Data_processed/Dataset_COVID_confiremed_complete.csv', index_col = [0])
    df_death= pd.read_csv('Data_processed/Dataset_COVID_Death_complete.csv', index_col=[0])
    df_recovered= pd.read_csv('Data_processed/Dataset_COVID_recovered_complete.csv', index_col=[0])
    df_population = pd.read_csv('Data_processed/population.csv', index_col=[0])
    return df_cases,df_death,df_recovered,df_population

df_cases,df_death,df_recovered,df_population = load_data()
country_choice = []

def df_selection(list_countries_temp, type,df_cases,df_death,df_recovered):
    list_countries_temp[0].append('Date')
    columns_to_filter = list_countries_temp[0]
    if (type =='Death'):
        return df_death[columns_to_filter]
    elif (type == 'Recovered'):
        return df_recovered[columns_to_filter]
    elif (type == 'Confirmed'):
        return df_cases[columns_to_filter]

def vis(filter_data,list_countries,dt_choice_normal, start_date, end_date,df_pop):
    filter_data['Date'] = pd.to_datetime(filter_data['Date'], format='%m/%d/%y')
    filter_data = filter_data.loc[(filter_data['Date'] >= start_date) & (filter_data['Date'] <= end_date),:]
    print(filter_data.head())
    if (dt_choice_normal =='Non-normalized data'):
        if (len(list_countries[0])<3):
            fig = px.line(filter_data, x='Date', y=list_countries[0][0] ,width=750, height=550, template= '%s' %(dt_choice_template))  # 'Daily_France_death')

            return fig
        elif (len(list_countries[0])>2):
            fig = px.line(filter_data, x='Date', y=filter_data.columns[0:-1],width=750, height=550, template= '%s' %(dt_choice_template))
            return fig
    elif(dt_choice_normal=='Normalized over 100k'):

        if (len(list_countries[0]) < 3):
            df_pop= df_pop.reset_index()
            population = df_pop[df_pop['Country (or dependency)']==list_countries[0][0]]['Population (2020)']
            count_1000 = int(population)/100000
            filter_data[list_countries[0][0]] = filter_data[list_countries[0][0]]/count_1000
            fig = px.line(filter_data, x='Date', y=list_countries[0][0],width=750, height=550, template= '%s' %(dt_choice_template))  # 'Daily_France_death')

            return fig
        elif (len(list_countries[0]) > 2):
            df_pop = df_pop.reset_index()
            for i in range(0,len(list_countries[0])-1):
                population = df_pop[df_pop['Country (or dependency)'] == list_countries[0][i]]['Population (2020)']
                count_1000 = int(population) / 100000
                filter_data[list_countries[0][i]] = filter_data[list_countries[0][i]]/count_1000
            fig = px.line(filter_data, x='Date', y=filter_data.columns[0:-1],width=750, height=550, template= '%s' %(dt_choice_template))
            return fig


# A Sidebar for choosing different functions
st.sidebar.subheader("Choosing Dates")
#year_2020 = st.sidebar.checkbox('2020')
#year_2021 = st.sidebar.checkbox('2021')
#month = st.sidebar.slider('Month',1,12,6)
start_date = pd.Timestamp(st.sidebar.date_input('Start date', datetime.date(2020,1,22), min_value=datetime.date(2020,1,22), max_value=datetime.date(2021,5,19)))
end_date = pd.Timestamp(st.sidebar.date_input('End date', datetime.date(2021,5,20), min_value=datetime.date(2020,1,23), max_value=datetime.date(2021,5,20)))

if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date: `%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start dat‚e.')

dt_choice_template =st.sidebar.selectbox("Choose Template", ['plotly','ggplot2', 'seaborn', 'simple_white',
         'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
         'ygridoff', 'gridon', 'none'])
country_choice.append(st.sidebar.multiselect("Choose countries", list(df_cases.columns[0:-3]), default='US'))
dt_choice = st.sidebar.selectbox("Choose Category", ['Confirmed','Death','Recovered'])
dt_choice_normal =st.sidebar.selectbox("Choose View", ['Normalized over 100k','Non-normalized data'])

if not country_choice:
    st.sidebar.error("Please select at least one country.")
    #country_choice.append('US')
if not dt_choice:
    st.sidebar.error("Please select at least one category.")
    #dt_choice = 'confirmed'
if not dt_choice_normal:
    st.sidebar.error("Please select number view.")

'##   Daily Cases for %s' %(dt_choice)

# Data Viz

data_to_plot = df_selection(country_choice, dt_choice,df_cases,df_death,df_recovered)
fig = vis(data_to_plot,country_choice,dt_choice_normal,start_date, end_date, df_population)
st.plotly_chart(fig)
