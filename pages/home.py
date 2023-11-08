import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path='/',
    top_nav=True
)

MARKDOWN = """
                [![Benoit Profile](https://img.shields.io/badge/Made%20with-Benoit%20Marchadier-brightgreen)](https://github.com/bebe0106)
                [![Antoine Profile](https://img.shields.io/badge/Made%20with-Antoine%20Aubert-blue)](https://github.com/Aubert-Antoine)
                
                
                **[GitHub project address](https://github.com/Projet-ESIEE/DashBoard-Energy)**
                
                Please find the **Developer Guide** and the **User Guide** for technical information and the **Rapport** for the analyses.
                
                ---
                
                # DashBoard Energy README :
                Please find below the different subsections of this page :
                
                1. [Introduction](#introduction)
                2. [Data](#data)
                3. [Data visualisation](#data-visualisation)
                4. [Pages](#pages)
                
                
                ## Introduction 
                This app is a dashboard that allows you to visualize the evolution of the energy consumption of the world's countries over the last 20 years. 
                This project is part of the Data Science course of the Master 2 of the ESIEE program, in the [data visualisation unit](https://perso.esiee.fr/~courivad/DSIA4101A/).
                
                ## Data
                The data used in this project comes from 3 different sources, available bellow in this page. They are all in open source and free to use.
                The main file is **kaggle : sustainable energy** and it is enhanced by the other files. One contain the HDI, and the other the continent and sub-regions of each country. 
                The goal is to get all the data needed to show interesting graphs, and deduct some relevant information from them.
                
                The data are cleaned and processed in the [process_data.py]() file. The data are then stored in the [dataset]() folder.
                
                Data set *1.* : [kaggle : sustainable energy](https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy) (500ko)
                
                Data set *2.* : [Our world in data : human development index](https://ourworldindata.org/human-development-index) (146ko)
                
                Data set *3.* : [Country to continent](https://www.kaggle.com/datasets/statchaitya/country-to-continent/data) (16ko)
                
                #### Description of the data set *1.* :
                > Uncover this comprehensive dataset showcasing sustainable energy indicators and other useful factors 
                > across all countries from 2000 to 2020. Dive into vital aspects such as electricity access, renewable energy, 
                > carbon emissions, energy intensity, Financial flows, and economic growth. Compare nations, track progress 
                > towards Sustainable Development Goal 7, and gain profound insights into global energy consumption patterns 
                > over time.
                
                
                #### Key Features of the data set *1.* : 
                * Entity: The name of the country or region for which the data is reported.
                * Year: The year for which the data is reported, ranging from 2000 to 2020.
                * Access to electricity (% of population): The percentage of population with access to electricity.
                * Access to clean fuels for cooking (% of population): The percentage of the population with primary reliance on clean fuels.
                * Renewable-electricity-generating-capacity-per-capita: Installed Renewable energy capacity per person
                * Financial flows to developing countries (US $): Aid and assistance from developed countries for clean energy projects.
                * Renewable energy share in total final energy consumption (%): Percentage of renewable energy in final energy consumption.
                * Electricity from fossil fuels (TWh): Electricity generated from fossil fuels (coal, oil, gas) in terawatt-hours.
                * Electricity from nuclear (TWh): Electricity generated from nuclear power in terawatt-hours.
                * Electricity from renewables (TWh): Electricity generated from renewable sources (hydro, solar, wind, etc.) in terawatt-hours.
                * Low-carbon electricity (% electricity): Percentage of electricity from low-carbon sources (nuclear and renewables).
                * Primary energy consumption per capita (kWh/person): Energy consumption per person in kilowatt-hours.
                * Energy intensity level of primary energy (MJ/$2011 PPP GDP): Energy use per unit of GDP at purchasing power parity.
                * Value_co2_emissions (metric tons per capita): Carbon dioxide emissions per person in metric tons.
                * Renewables (% equivalent primary energy): Equivalent primary energy that is derived from renewable sources.
                * GDP growth (annual %): Annual GDP growth rate based on constant local currency.
                * GDP per capita: Gross domestic product per person.
                * Density (P/Km2): Population density in persons per square kilometer.
                * Land Area (Km2): Total land area in square kilometers.
                * Latitude: Latitude of the country's centroid in decimal degrees.
                * Longitude: Longitude of the country's centroid in decimal degrees.
                
                
                ## Data visualisation
                The web application is served by a Dash server. It is a tool to display [plotly](https://plotly/python.com) graphs. 
                The principle is to chose thanks to 'Multi-Select Dropdown' the area you would like to display. 
                Then all the graph should be updated, for the selection. 
                
                ## Pages
                The app is composed of 5 pages :
                - **Home** : This current page.
                - **Missing values analytics** : analyse the missing values of the dataset and visualisez the global trend via a few plots. 
                - **Maps & histogram analytics** : 
                - **User Guide** : which lets you deploy and use your dashboard on another machine
                - **Report** : which highlights the main conclusions drawn from the data.
                - **Developer Guide** : which allows you to understand the architecture of the code and modify or extend it.
            """

layout = html.Div(
    className="content",
    children=[
        html.H1('This is our Home page'),
        dcc.Markdown(MARKDOWN)
])

