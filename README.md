Table of Content
================
* [Interactive-Covid-19-Dashboard](#Interactive-Covid-19-Dashboard)
  * [Description](#description)
  * [Datasets](#Datasets)
  * [Installation guide](#installation-guide)
  * [Licensing](#licensing)

# Interactive-Covid-19-Dashboard
https://share.streamlit.io/soledadli/interactive-covid-19-dashboard/main/app.py

## Description
A collaborative work of building an interactive Covid-19 dashboard to provide insights about COVID globally by students from the Digital Sciences Track of Center for Research and Interdiscplinarity. 

## Datasets
The data sets are from the open data of [Jonhs Hopkins University](https://github.com/CSSEGISandData/COVID-19)
* Dataset_COVID_Death_complete.csv
* Dataset_COVID_confiremed_complete.csv
* Dataset_COVID_recovered_complete.csv

each of the files has the following columns:
Country / region: identifies the name of the country in English.
Province / state: identifies the name of the states in English that make up countries such as China, Canada, Australia or overseas territories such as Denmark, the Netherlands or France.
latitude: is one of the geographic coordinates that specifies the north – south position of a point on the Earth's surface.
Longitude: it is one of the geographic coordinates that specifies the east – west position of a point on the Earth's surface.
Date: identifies the accumulated cases per day in each of the countries.
- To calulcate the normalization we acquire to get the population of the each country https://www.kaggle.com/tanuprabhu/population-by-country-2020 and we only used Country and Population. 

## Installation Requirements
To install the project dependencies run pip install -r requirements.txt
```
pip install -r requirements.txt
```
Requirements includees:
```
pandas == 1.2.4
streamlit==0.82.0
plotly==4.14.3
```
To run the streamlit code
```
streamlit run app.py
```

## Licensing
MIT License

Dashboard Designers:
Dana Almanla
Xiaojing(Soledad) Li
Eliseo Baquero
