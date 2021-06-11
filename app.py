import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Setting Dashboard Interface
st.set_page_config(layout="wide")

st.title('🦠COVID-19 Dashboard')
st.markdown(
'''A collaborative work of building an interactive Covid-19 dashboard to provide insights about COVID globally. [GitHub Project](https://github.com/soledadli/interactive-Covid-19-dashboard)\n
The data is from 01.22.2020 to 05.20.2021 and is collected from the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University. Data source: [COVID-19 Data Repository](https://github.com/CSSEGISandData/COVID-19) ''')

st.subheader("Information about the features.")


with st.beta_expander("Explanation & Tips"):
     st.markdown(""" The COVID-19 Dashboard includes the following 6 features for data visualization. \n
     1. Choose Template of the plots.
     2. Choose a time frame.
     3. Choose countries
     4. Choose categories from three types of cases: 
        confirmed deaths, confirmed, and recovered.
     5. Choose case view: daily cases or cumulative cases.
     6. Choose view between normalized over 100k and non-normalized data. 
     Tip 1: The graph includes the rolling average of seven last days.
     Tip 2: To compare two or more countries in absolute numbers, 
        it is better to use the option 'Non-normalized data.'
        To compare two or more countries with significant differences in population, 
        the best option is 'Normalized over 100k'.""")

# Experimenting with Data
@st.cache
def load_data( ):
    df_cases = pd.read_csv('Data_processed/Dataset_COVID_confiremed_complete.csv', index_col = [0])
    df_death= pd.read_csv('Data_processed/Dataset_COVID_Death_complete.csv', index_col=[0])
    df_recovered= pd.read_csv('Data_processed/Dataset_COVID_recovered_complete.csv', index_col=[0])
    df_population = pd.read_csv('Data_processed/population.csv', index_col=[0])
    df_location = pd.read_csv('time_series_covid19_confirmed_global.csv', index_col=[0])
    return df_cases,df_death,df_recovered,df_population,df_location

df_cases,df_death,df_recovered,df_population,df_location = load_data()
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

def vis(filter_data,list_countries,dt_choice_normal, dt_choice_cases, start_date, end_date,df_pop):
    filter_data['Date'] = pd.to_datetime(filter_data['Date'], format='%m/%d/%y')
    filter_data = filter_data.loc[(filter_data['Date'] >= start_date) & (filter_data['Date'] <= end_date),:]

    if (dt_choice_normal == 'Non-normalized data'):
        if (dt_choice_cases == "Daily Cases"): # view choices
            if (len(list_countries[0]) < 3):
                filter_data['Average'] = filter_data.iloc[:, 0].rolling(7).mean() # 7 day average calculation

                fig = px.line(filter_data, x='Date', y=list_countries[0][0], 
                              width=1000, height=500, template= '%s' %(dt_choice_template))  # 'Daily_France_death')
                return fig

            elif (len(list_countries[0]) > 2):
               # for i in filter_data.columns[0:-1]:
               #     new_col = '7-day-rolling-' + i
               #     filter_data[new_col] = filter_data.loc[:, i].rolling(7).mean() # 7 day average calculation
               # print(filter_data.columns[len(list_countries[0]):])

                fig = px.line(filter_data, x='Date', y=filter_data.columns[0:len(list_countries[0])],
                                  width=1000, height=500, template= '%s' %(dt_choice_template))

                #for i in filter_data.columns[len(list_countries[0]):]:
                #    fig.add_bar(x=filter_data['Date'], y=filter_data[i] , name = i)
                return fig

        if (dt_choice_cases == "7-day rolling"): # 7-day rolling
            if (len(list_countries[0]) < 3):
                filter_data['Average'] = filter_data.iloc[:, 0].rolling(7).mean() # 7 day average calculation

                fig = px.line(filter_data, x=filter_data['Date'], y=filter_data['Average'],
                              width=1000, height=500, template='%s' % (dt_choice_template))  # 'Daily_France_death')
                return fig

            elif (len(list_countries[0]) > 2):
                for i in filter_data.columns[0:-1]:
                    new_col = '7-day-rolling-' + i
                    filter_data[new_col] = filter_data.loc[:, i].rolling(7).mean()  # 7 day average calculation

                fig = px.line(filter_data, x='Date', y=filter_data.columns[len(list_countries[0]) :],
                              width=1000, height=500, template='%s' % (dt_choice_template))

                return fig

        if (dt_choice_cases == "Cumulative Cases"):
            filter_data['Cumulative'] = filter_data.iloc[:, 0].cumsum()  # Cumulative Cases Calculation
            if (len(list_countries[0]) < 3):
                fig = px.line(filter_data, x='Date', y='Cumulative', width=1000,
                              height=500)  # Cumulative Cases Plot
                return fig

            elif (len(list_countries[0]) > 2):
                for i in filter_data.columns[0:-2]:
                    new_col = 'Cumulative' + i
                    filter_data[new_col] = filter_data.loc[:, i].cumsum()

                fig = px.line(filter_data, x='Date', y=filter_data.columns[(len(list_countries[0])+1):], 
                              width=1000, height=500, template= '%s' %(dt_choice_template))
                return fig


    elif(dt_choice_normal=='Normalized over 100k'):
        if (dt_choice_cases == "Daily Cases"):
            if (len(list_countries[0]) < 3):
                df_pop= df_pop.reset_index()
                population = df_pop[df_pop['Country (or dependency)']==list_countries[0][0]]['Population (2020)']
                count_1000 = int(population)/100000
                filter_data[list_countries[0][0]] = filter_data[list_countries[0][0]]/count_1000
                filter_data['Average'] = filter_data.iloc[:, 0].rolling(7).mean() # 7_day_average Calculation

                fig = px.line(filter_data, x='Date', y=list_countries[0][0],
                              width=1000, height=500, template= '%s' %(dt_choice_template))
                # fig.add_bar(x=filter_data['Date'], y=filter_data['Average'], name='7 days Average') # 7_day_average plot

                return fig

            elif (len(list_countries[0]) > 2):
                df_pop = df_pop.reset_index()
                for i in range(0,len(list_countries[0])-1):
                    population = df_pop[df_pop['Country (or dependency)'] == list_countries[0][i]]['Population (2020)']
                    count_1000 = int(population) / 100000
                    filter_data[list_countries[0][i]] = filter_data[list_countries[0][i]]/count_1000
                for i in filter_data.columns[0:-1]:
                    new_col = '7-day-rolling-' + i
                    filter_data[new_col] = filter_data.loc[:, i].rolling(7).mean()  # 7 day average calculation
                    # print(filter_data.columns[len(list_countries[0]):])

                fig = px.line(filter_data, x='Date', y=filter_data.columns[0:len(list_countries[0])],
                              width=1000, height=500, template= '%s' %(dt_choice_template))

                return fig

        if (dt_choice_cases == "7-day rolling"):
            if (len(list_countries[0]) < 3):
                df_pop= df_pop.reset_index()
                population = df_pop[df_pop['Country (or dependency)']==list_countries[0][0]]['Population (2020)']
                count_1000 = int(population)/100000
                filter_data[list_countries[0][0]] = filter_data[list_countries[0][0]]/count_1000
                filter_data['Average'] = filter_data.iloc[:, 0].rolling(7).mean() # 7_day_average Calculation

                fig = px.line(x=filter_data['Date'], y=filter_data['Average'],width=1000, height=500, template= '%s' %(dt_choice_template))  # 7_day_average plot

                return fig

            elif (len(list_countries[0]) > 2):
                df_pop = df_pop.reset_index()
                for i in range(0, len(list_countries[0]) - 1):
                    population = df_pop[df_pop['Country (or dependency)'] == list_countries[0][i]]['Population (2020)']
                    count_1000 = int(population) / 100000
                    filter_data[list_countries[0][i]] = filter_data[list_countries[0][i]] / count_1000
                for i in filter_data.columns[0:-1]:
                    new_col = '7-day-rolling-' + i
                    filter_data[new_col] = filter_data.loc[:, i].rolling(7).mean()  # 7 day average calculation
                    # print(filter_data.columns[len(list_countries[0]):])

                fig = px.line(filter_data, x='Date', y=filter_data.columns[len(list_countries[0]) :], width=1000, height=500, template='%s' % (dt_choice_template))

                return fig


        if (dt_choice_cases == "Cumulative Cases"):
            if (len(list_countries[0]) < 3):
                df_pop = df_pop.reset_index()
                population = df_pop[df_pop['Country (or dependency)'] == list_countries[0][0]]['Population (2020)']
                count_1000 = int(population) / 100000
                filter_data[list_countries[0][0]] = filter_data[list_countries[0][0]] / count_1000
                filter_data['Cumulative'] = filter_data.iloc[:, 0].cumsum()  # Cumulative Cases Calculation

                fig = px.line(filter_data, x='Date', y='Cumulative',width=1000, height=500, template= '%s' %(dt_choice_template))  # Cumulative Cases Plot

                return fig

            elif (len(list_countries[0]) > 2):
                df_pop = df_pop.reset_index()
                for i in range(0, len(list_countries[0]) - 1):
                    population = df_pop[df_pop['Country (or dependency)'] == list_countries[0][i]]['Population (2020)']
                    count_1000 = int(population) / 100000
                    filter_data[list_countries[0][i]] = filter_data[list_countries[0][i]] / count_1000
                print(filter_data.head())
                for i in filter_data.columns[0:-1]:
                    new_col = 'Cumulative' + i
                    filter_data[new_col] = filter_data.loc[:, i].cumsum()

                fig = px.line(filter_data, x='Date', y=filter_data.columns[len(list_countries[0]) :], 
                              width=1000, height=500, template= '%s' %(dt_choice_template),

                              )

                return fig
def map_view(df_loca,country_choice,type,df_cases,df_death,df_recovered,dt_choice_normal, dt_choice_cases, start_date, end_date,df_pop):

    df_loca_sub = df_loca[['Country/Region','Lat','Long']]
    if (type =='Death'):
        data_to_work = df_death.copy()
    elif (type == 'Recovered'):
        data_to_work = df_recovered.copy()
    elif (type == 'Confirmed'):
        data_to_work= df_cases.copy()
    data_to_work['Date'] = pd.to_datetime(data_to_work['Date'], format='%m/%d/%y')
    data_to_work = data_to_work.loc[(data_to_work['Date'] >= start_date) & (data_to_work['Date'] <= end_date), :]
    data_to_work = data_to_work.drop(columns={'Date', 'month', 'year'})
    data_to_work = data_to_work.sum()

    data_to_work = data_to_work.reset_index().rename(columns={'index': 'Country/Region', 0: 'Total'})
    data_to_work_full = data_to_work.merge(df_loca_sub, how='left', on='Country/Region')

    df_pop = df_pop.reset_index().rename(columns={'Country (or dependency)': 'Country/Region'})
    df_pop['count_10000'] = df_pop['Population (2020)'] / 100000
    data_to_work_full_pop = data_to_work_full.merge(df_pop, how='left', on='Country/Region')
    data_to_work_full_pop['Normalized data'] = data_to_work_full_pop['Total']/data_to_work_full_pop['count_10000']
    data_to_work_full_pop = data_to_work_full_pop.drop_duplicates(subset=['Country/Region'], keep='first')
    data_to_work_full_pop.at[119, 'Lat'] =  48.864716
    data_to_work_full_pop.at[119, 'Long']= 2.349014
    data_to_work_full_pop['color_pop'] = ''
    print(country_choice)
    data_to_work_full_pop['color_pop'] = data_to_work_full_pop["Country/Region"].apply(lambda x: 'Selected' if x in country_choice[0] else 'Not Selected')

    if (dt_choice_normal=='Non-normalized data'):
        fig =  px.scatter_mapbox(data_to_work_full_pop, lat="Lat", lon = 'Long',size="Total",  # size of markers, "pop" is one of the columns of gapminder
                             template='%s' % (dt_choice_template),zoom=1,hover_name = "Country/Region",  color='color_pop'

                                ,hover_data = {'Normalized data':True,'Total':True,'Lat' : False,'Long':False})
        fig.update_layout(mapbox_style="open-street-map",width=1270,showlegend=False)
        #fig.update_layout(margin={"r": 0, "l": 0})
        return fig
    elif(dt_choice_normal=='Normalized over 100k'):
        fig = px.scatter_mapbox(data_to_work_full_pop, lat="Lat", lon='Long', size="Normalized data",
                                # size of markers, "pop" is one of the columns of gapminder
                                template='%s' % (dt_choice_template), zoom=1,hover_name = "Country/Region",color='color_pop'
                                ,hover_data = {'Normalized data':True,'Total':True,'Lat' : False,'Long':False})
        fig.update_layout(mapbox_style="open-street-map",width=1270,showlegend=False)
       # fig.update_layout(margin={"r": 0, "l": 0})

        return fig



    #fil_data['Cumulative'] = fil_data.iloc[:, 0].cumsum()



dt_choice_template =st.sidebar.selectbox("Choose Template", ['plotly','ggplot2', 'seaborn', 'simple_white',
         'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
         'ygridoff', 'gridon', 'none'])
# A Sidebar for choosing different functions
st.sidebar.subheader("Choosing Dates")
#year_2020 = st.sidebar.checkbox('2020')
#year_2021 = st.sidebar.checkbox('2021')
#month = st.sidebar.slider('Month',1,12,6)
start_date = pd.Timestamp(st.sidebar.date_input('Start date', datetime.date(2020,1,22), min_value=datetime.date(2020,1,22), max_value=datetime.date(2021,5,19)))
end_date = pd.Timestamp(st.sidebar.date_input('End date', datetime.date(2021,5,20), min_value=datetime.date(2020,1,23), max_value=datetime.date(2021,5,20)))



dt_choice = st.sidebar.selectbox("Choose Category", ['Confirmed','Death','Recovered'])
dt_choice_cases = st.sidebar.selectbox("Choose Case View", ['7-day rolling','Daily Cases', 'Cumulative Cases'])
dt_choice_normal =st.sidebar.selectbox("Choose View", ['Normalized over 100k','Non-normalized data'])
dt_country = st.sidebar.multiselect("Choose countries", list(df_cases.columns[0:-3]), default=['US','Italy'])
country_choice.append(dt_country)
#country_choice.append(st.sidebar.multiselect("Choose countries", list(df_cases.columns[0:-3]), default='US'))
if not dt_country:
    st.error("Please select at least one country.")
    st.stop()



fig_map = map_view(df_location,country_choice,dt_choice,df_cases,df_death,df_recovered,dt_choice_normal, dt_choice_cases, start_date, end_date,df_population)
st.plotly_chart(fig_map)
if not dt_choice:
    st.sidebar.error("Please select at least one category.")
    #dt_choice = 'confirmed'
if not dt_choice_normal:
    st.sidebar.error("Please select number view.")

'## %s for  %s' %(dt_choice_cases, dt_choice)

# Data Viz


data_to_plot = df_selection(country_choice, dt_choice,df_cases,df_death,df_recovered)
#print(data_to_plot.head())
fig = vis(data_to_plot,country_choice,dt_choice_normal,dt_choice_cases, start_date, end_date, df_population)
fig.update_layout(width=1300, height=500)
st.plotly_chart(fig)
