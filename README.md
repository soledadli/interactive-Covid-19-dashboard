Table of Content
================
* [Interactive-Covid-19-Dashboard](#Interactive-Covid-19-Dashboard)
  * [Description](#description)
  * [Datasets](#datasets)
  * [Installation Requirements](#installation-requirements)
  * [Software Heritage](#software-heritage)
  * [Licensing](#licensing)
  * [Authors](#Authors)

# Interactive-Covid-19-Dashboard
https://share.streamlit.io/soledadli/interactive-covid-19-dashboard/main/app.py

## Description
A collaborative work of building an interactive Covid-19 dashboard to provide insights about COVID globally by students from the Digital Sciences Track of Center for Research and Interdiscplinarity. 

## Datasets
The data sets are from the open data of [Jonhs Hopkins University](https://github.com/CSSEGISandData/COVID-19)
* Dataset_COVID_Death_complete.csv
* Dataset_COVID_confiremed_complete.csv
* Dataset_COVID_recovered_complete.csv

Columns in the datasets:

- `Country / region`: identifies the name of the country
- `Province / state`: identifies the name of the states
- `Latitude`: the geographic coordinates that specifies the north – south position of a point on the Earth's surface.
- `Longitude`: the geographic coordinates that specifies the east – west position of a point on the Earth's surface.
- `Date`: identifies the cumulative cases per day in each of the countries.

To calulcate the normalization we acquire to get the population of the each country https://www.kaggle.com/tanuprabhu/population-by-country-2020 and we only used `Country and Population`. 


## Installation Requirements
- Download Zip
```
Code - Download ZIP
```

- Clone this repository with this command
```
git clone https://github.com/soledadli/interactive-Covid-19-dashboard.git
```
- Install the project dependencies run pip install -r requirements.txt
```
pip install -r requirements.txt
```
- Requirements includes:
```
pandas == 1.2.4
streamlit==0.82.0
plotly==4.14.3
```
To run the streamlit code
```
streamlit run app.py
```
## Software Heritage
[![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:f16dc74c8cb24abe9674c52b352154a7eecaabaa/)](https://archive.softwareheritage.org/swh:1:dir:f16dc74c8cb24abe9674c52b352154a7eecaabaa;origin=https://github.com/soledadli/interactive-Covid-19-dashboard.git;visit=swh:1:snp:2cf6701fa76c93de35a2755c576ce5a4060d5b79;anchor=swh:1:rev:37f7e56df4be5edc7df6a6c12b21e7463b0c9fcc)

## Licensing
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Authors:
* **Dana Almanla** [@Danaal](https://github.com/Danaal) 
* **Xiaojing(Soledad) Li** [@soledadli](https://github.com/soledadli) 
* **Eliseo Baquero** [@Eli-2020](https://github.com/Eli-2020)
