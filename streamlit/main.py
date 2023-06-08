import streamlit as st
from streamlit_option_menu import option_menu


import sys
import os
from funciones import *
import pandas as pd
import numpy as np
import math
from itertools import cycle
import base64
import time

pd.options.plotting.backend = "plotly"
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib.animation import FuncAnimation


st.set_page_config(page_title="Go vegan?", page_icon=":avocado:", layout="wide", initial_sidebar_state="expanded")


fod = pd.read_csv('data/Food/food_clean.csv')
soy = pd.read_csv(r'..\data\Soy\soy_clean.csv', parse_dates=['Year'])
oil_prod = pd.read_csv(r'..\data/Palm/oil_prod_clean.csv')
oil_yield = pd.read_csv(r'..\data/Palm/oil_yield_clean.csv')
pop = pd.read_csv(r'..\data/Population/population_clean.csv')

# filtro para sacar lista de sólo paises
todos = soy['Entity'].value_counts().index.to_list()
paises = filtrar_paises(todos)

palette = ['#6a863b', '#68c843', '#f39f18']

# CSS access
with open('style.css') as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )

# Sidebar menu
with st.sidebar:
    
    st.image('../images/streamlit/logor.png', width=30)
    opcions = ['Home', 'General overview', 'Explore', 'Recomendations', 'About us']
    selected = option_menu("Menu", opcions, 
        icons=['house', 'folder', 'graph-up', 'eye', 'flower2'], menu_icon="cast", default_index=0)

    with st.spinner("Loading..."):
        time.sleep(2)



if selected == 'Home':

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.write('               ')
    with col2:
        st.image('../images/streamlit/logof.png', width=210)

    st.write('\n')    
    st.subheader("Are you aware of your impact?")
    st.write("---")

    col1, col2 = st.columns([2.75, 1])

    with col1:
        st.write("🌱🌍 Dive into the Impact of Your Food Choices 🍽️")
        st.write("Climate change is a pressing concern that demands our attention. As **global warming** becomes an imminent issue, the scarcity of water looms and our reliance on fossil fuels reaches a critical point.")
        st.write("But fear not! We are determined to combat. And guess what? One of the most effective steps we can take is right in front of us—**our diet**.")
        st.write("Did you know that the food we consume daily holds a significant influence over the environment? In a groundbreaking report by the UN's Intergovernmental Panel on Climate Change (IPCC), it was revealed that the **high consumption of meat and dairy in the Western world is contributing to global warming**. It's time for us to reassess our choices and embrace a more eco-friendly approach to eating.")
        st.write("In this web, you´ll get to know the emissions, water waste and other info about your usual meals. Join us on this adventure as we uncover the answers and discover the **power of veganism as the ultimate eco-friendly dietary choice**.")
        st.write("Are you ready to discover how veganism can revolutionize your life and help save the planet? Let's get started!")

    with col2:
        st.write('\n')
        st.write('\n')
        st.write("\n")
        ruta = r'..\images\streamlit\food.png'
        st.image(ruta, clamp=True)


if selected == 'General overview':
    st.subheader("Check the emissions of your meals 🌱")
    st.write("**Total greenhouse gas emissions¹** of the most tipical foods around the world. Let´s dive in!")
    st.write("You can compare them by animal or vegetable origin, or you can simply select the specific labels that interest you.")


    # Gráfico de todas las food
    # Cálculo de las emisiones totales de comida
    fod['Total_Food_Emissions'] = fod.iloc[:, 2:9].sum(axis=1)

    # Ordenar el DataFrame por las emisiones totales
    df_sorted = fod.sort_values('Total_Food_Emissions', ascending=True)

    # Lista de colores
    n_colors = 43  
    # palette = sns.color_palette("bright", n_colors)
    palette = ["#FF5722", "#AED581", "#D0ECE7", "#9CCC65", "#C5E1A5", "#FFAB91", "#FFE0B2",  
            "#DCEDC8", "#FF8A65", "#FFCCBC", "#7CB342", "#DCE775", "#FF7043", "#FFAB40", 
            "#689F38", "#D4E157", "#FF5722", "#558B2F", "#CDDC39", "#E64A19", "#8BC34A",
            "#FF6E40", "#33691E", "#AFB42B", "#BF360C", "#FF3D00", "#827717", "#C0CA33", 
            "#FFAB00", "#827717", "#AFB42B", "#BF360C", "#FF3D00", "#827717", "#C0CA33", 
            "#FFAB00", "#795548", "#A1887F", "#3E2723", "#795548", "#A1887F", "#3E2723", "#3E2723"]


    # Crear la figura
    fig = go.Figure()

    # Crear una lista de barras utilizando go.Bar para cada entidad
    data = []
    for i, row in df_sorted.iterrows():
        entity = row['Entity']
        bar = go.Bar(
            x=[row['Total_Food_Emissions']],
            y=[entity],
            orientation='h',
            visible=True,
            marker=dict(color=palette[i]),
            name=entity  # Asignar el nombre de la entidad a la barra
        )
        fig.add_trace(bar)
        



    # Configuración del diseño del gráfico
    fig.update_layout(
        title='Global CO emissions by food',
        xaxis=dict(
            title='Total emissions',
            title_font=dict(color='#59412f')),
        yaxis=dict(
            title='Food',
            title_font=dict(color='#59412f')),
        legend=dict(x=1.02, y=1,
                    title_font=dict(color='#59412f'),
                    font=dict(color='#59412f')),
        height=500,
        width=800,
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=[{"visible": [True if x else False for x in df_sorted['Animal_origin']]}],
                        label="Animal Origin",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [True if not x else False for x in df_sorted['Animal_origin']]}],
                        label="Vegetable Origin",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [True] * len(df_sorted)}],
                        label="All Entities",
                        method="update"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.7,
                xanchor="left",
                y=1.2,
                yanchor="top",
                bgcolor="#6a863b",
                active=2,
                font=dict(color='#F5F5DC')
            
            ),
        ]
    )

    # Ordenar las barras en el eje Y
    fig.update_yaxes(
        tickfont=dict(color='#6C584C'),
        type='category',
        categoryorder='array',
        categoryarray=df_sorted['Entity']
    )

    # Exe x
    fig.update_xaxes(
        tickfont=dict(color='#7E675E')  # Cambia el color de las etiquetas del eje x a rojo
    )

    st.plotly_chart(fig, theme="streamlit")

    col1, col2 = st.columns([6, 1])
    with col1:
        st.write("\n")
        st.write("**Do you want to know more?** Let´s go to Explore!")
    # clicked = st.button(label='Click here', )
    # if clicked:
    #     st.experimental_set_query_params(selected="Explore")
    with col2:
        st.image('../images/streamlit/logor.png', width=40)

    st.write("---")
    st.write("¹Greenhouse gas emissions: is a unit in CO2eq that converts the impact of different kinds of greenhouse gases, like methane and nitrous oxide, to the equivalent amount of carbon dioxide.")


if selected == 'Explore':

    st.subheader("Discover your food choices environmental impact 🌱")
    st.write("To find out the climate impact of what you eat and drink, **choose from one of the items in our calculator** 🡳")
    # Food specifications
    food_l = ["Take your pick!", "Meat", "Vegetable oils", "Soy", "Dark Chocolate", "Sugar", "Coffee", "Vegetables", "Fruits", "Rice"]
    opcion = st.selectbox('Which food are you interested in the most?', food_l)
    st.write("---")

    if opcion == 'Soy':

        st.subheader("Let's dive into the world of soy")

        st.write("⚡**Fun fact**: There are health benefits to soy, which include providing a good source of *heart-healthy fats*, *fiber*, *potassium* and *iron*.")
        st.write("But not everything is sunshine 🌞 and rainbows 🌈. Soy is one of the main causes of deforestation in South America. But, what for is destined the soybean production?")

        # Comparative graphic between soybeans for food, feed or processed
        # new df filtered from 2000
        df = soy[soy['Year'].dt.year >= 2000]
        totals = df[['Food', 'Feed', 'Processed']].sum()

        # Colors and labels
        colors = ['#FF5722', '#AED581', '#D0ECE7']
        labels = ['Food', 'Feed', 'Processed']

        # Create figure
        fig = go.Figure()

        # Create vertical bars
        fig.add_trace(
            go.Bar(
                x=labels,
                y=totals,
                marker=dict(color=colors),
                name='Total emissions',
                hovertemplate=[f'{label}: {value}' for label, value in zip(labels, totals)],
            )
        )

        # Configure chart layout
        fig.update_layout(
            title='Total emissions by soy use',
            xaxis=dict(
                title='Soy use',
                title_font=dict(color='#59412f')
            ),
            yaxis=dict(
                title='Total emissions',
                title_font=dict(color='#59412f'),
                range=[0, max(totals) + max(totals) * 0.1]
            ),
            height=400,
            width=600,
            showlegend=False
        )

        # Configure axis
        fig.update_yaxes(tickfont=dict(color='#6C584C'))
        fig.update_xaxes(tickfont=dict(color='#7E675E'))

        # Display chart
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("**Legend**:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("- Food: human consume.")
        with col2: 
            st.write("- Feed: animal feed.")
        with col3:
            st.write("- Processed: used for productions.")
        st.write("---")
        st.write("\n")
        st.write("\n")
        st.write("**Wow! The difference between them is surprising**. The processed soy is the main destined use by far. Some examples from what soy can be processed are **soy oil** or **soybean cake** for basic animal feed protein")
        st.write("---")

        st.subheader("What is the surface area covered by this macroharvest?")


        # Graphic: hectares by country
        # Filtered for just countries
        df_filtered = soy[soy['Entity'].isin(paises)]
        # Grouped for country and year and mean the harvested area
        grouped = df_filtered.groupby(['Entity', 'Year'])['Area harvested'].mean().reset_index()
        # Order descendent and filter for top 5
        top_countries = grouped.groupby('Entity')['Area harvested'].sum().nlargest(5).index
        df_top_countries = grouped[grouped['Entity'].isin(top_countries)]

        # Create interactive graphic
        fig = px.line(df_top_countries, x='Year', y='Area harvested', color='Entity',
                    labels={'Year': 'Year', 'Area harvested': 'Area harvested (hectareas)'},
                    title='Evolution of hectares harvested by top 5 countries')
        # Animation
        fig.update_layout(
            xaxis=dict(title_font=dict(color='#59412f'),
                    range=[df_top_countries['Year'].min(), df_top_countries['Year'].max()], autorange=False),
            yaxis=dict(
                title_font=dict(color='#59412f')),
            updatemenus=[
                dict(
                    type='buttons',
                    buttons=[
                        dict(label='Play',
                            method='animate',
                            args=[None, {'frame': {'duration': 200, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 200}}]),
                        dict(label='Pause',
                            method='animate',
                            args=[[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}])
                    ],
                    active=0,
                    showactive=True,
                    x=0.015,
                    y=0,
                    xanchor='right',
                    yanchor='bottom'
                )
            ]
        )
        # Animation photograms
        frames = []
        colors = ["#D4E157", "#FF5722", "#558B2F", "#CDDC39", "#E64A19"]
        for i, year in enumerate(df_top_countries['Year'].unique()):
            frame_data = df_top_countries[df_top_countries['Year'] <= year]
            frame = go.Frame(
                data=[go.Scatter(x=frame_data[frame_data['Entity'] == country]['Year'], 
                                y=frame_data[frame_data['Entity'] == country]['Area harvested'], 
                                mode='lines', 
                                name=country,
                                line=dict(color=colors[i % len(colors)]))  # Asignar color de la paleta
                    for country in top_countries],
                name=str(year)
            )
            frames.append(frame)
        fig.frames = frames

        # Config axis
        fig.update_yaxes(
            tickfont=dict(color='#6C584C'))
        fig.update_xaxes(
            tickfont=dict(color='#7E675E'))
        # Show
        st.plotly_chart(fig, use_container_width=True)

        st.write("In **Brazil** the production in 2020 was by **370k hectares**. That´s the equivalent for **370k football fields** or the whole surface of Mexico City")

        st.subheader("Check your consume impact 🍽️")
        st.write("The most common soy foods are **soy milk** and **tofu**")
        # Tofu and soy milk consumption
        col1, col2 = st.columns([1, 2])
        with col1:
            list_soy = ["Choose an option", "Soy milk", "Tofu"]
            soy_choice = st.selectbox("Select one!", list_soy)
        
        with col2:
            # consumption
            freq = ["Are you an usual consumer?", "Once a day", "1-2 times a week", "Never"]                
            choice = st.selectbox("How often do you have it?", freq)
            
        # SOY MILK
        if soy_choice == 'Soy milk':
            col1, col2 = st.columns([1.75, 2])
            col1.write('<style>.stRadio > label{height: 50px; display: flex; align-items: center;}</style>', unsafe_allow_html=True)
            col2.write('<style>.stRadio > label{height: 50px; display: flex; align-items: center;}</style>', unsafe_allow_html=True)

            # imagen tofu
            with col1:
                ruta_imagen = r'..\images\streamlit\soymilk.png'
                st.image(ruta_imagen, width=160, clamp=True)
                st.markdown("200ml per serving")

            with col2:

                if choice == "Once a day":
                    soy_milk_emissions = fod[fod['Entity'] == 'Soy milk']
                    # Total emisions of 200g by day
                    total_emissions = soy_milk_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                        'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                        'food_emissions_packaging', 'food_emissions_losses']].sum().sum() * 0.2
                    # Result
                    st.write(f"Over an entire year your consumption of soy milk is adding {math.ceil(total_emissions* 365)}kg greenhouse gas emissions.")
                    # GIF car
                    with open(r'..\images\streamlit\car.gif', 'rb') as r_ima:
                        contents = r_ima.read()
                    data_url = base64.b64encode(contents).decode("utf-8")
                    image_html = f'<img src="data:image/gif;base64,{data_url}" alt="car gif" style="width: 150px;">'
                    st.markdown(image_html, unsafe_allow_html=True)
                    st.write('\n')
                    st.markdown("That's the equivalent of driving **311km in car**")

                if choice == "1-2 times a week":
                    soy_milk_emissions = fod[fod['Entity'] == 'Soy milk']
                    # Total emisions of 200g by1,5 days week
                    total_emissions = soy_milk_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                        'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                        'food_emissions_packaging', 'food_emissions_losses']].sum().sum() * 0.2
                    # Result
                    st.write(f"Over an entire year your consumption of soy milk is adding {math.ceil(total_emissions* 78)}kg greenhouse gas emissions.")
                    # GIF car
                    with open(r'..\images\streamlit\car.gif', 'rb') as r_ima:
                        contents = r_ima.read()
                    data_url = base64.b64encode(contents).decode("utf-8")
                    image_html = f'<img src="data:image/gif;base64,{data_url}" alt="car gif" style="width: 150px;">'
                    st.markdown(image_html, unsafe_allow_html=True)
                    st.write('\n')
                    st.markdown("That's the equivalent of driving **69km in car**")

                if choice == "Never":
                    soy_milk_emissions = fod[fod['Entity'] == 'Soy milk']
                    # Total emisions of 42kg by year, global mean
                    total_emissions = soy_milk_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                        'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                        'food_emissions_packaging', 'food_emissions_losses']].sum().sum()
                    # Result
                    st.write(f"That's interesting, eventhough over an entire year the world average consumption of soy milk is adding {math.ceil(total_emissions* 42)}kg greenhouse gas emissions.")
                    # GIF car
                    with open(r'..\images\streamlit\car.gif', 'rb') as r_ima:
                        contents = r_ima.read()
                    data_url = base64.b64encode(contents).decode("utf-8")
                    image_html = f'<img src="data:image/gif;base64,{data_url}" alt="car gif" style="width: 150px;">'
                    st.markdown(image_html, unsafe_allow_html=True)
                    st.write('\n')
                    st.markdown("That's the equivalent of driving **177km in car**")
            
        # TOFU
        if soy_choice == 'Tofu':
            col1, col2 = st.columns([1.75, 2])
            col1.write('<style>.stRadio > label{height: 50px; display: flex; align-items: center;}</style>', unsafe_allow_html=True)
            col2.write('<style>.stRadio > label{height: 50px; display: flex; align-items: center;}</style>', unsafe_allow_html=True)

            # imagen tofu
            with col1:
                ruta_imagen = r'..\images\streamlit\tofua.png'
                st.image(ruta_imagen, width=160, clamp=True)
                st.markdown("150g per serving")            

            with col2:
                if choice == "Once a day":
                    tofu_emissions = fod[fod['Entity'] == 'Tofu']
                    # Total emisions of 150g by day
                    total_emissions = tofu_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                        'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                        'food_emissions_packaging', 'food_emissions_losses']].sum().sum() * 0.15
                    # Result
                    st.write(f"Over an entire year your consumption of tofu is adding {math.ceil(total_emissions* 365)}kg greenhouse gas emissions.")  

                    # GIF car
                    with open(r'..\images\streamlit\car.gif', 'rb') as r_ima:
                        contents = r_ima.read()
                    data_url = base64.b64encode(contents).decode("utf-8")
                    image_html = f'<img src="data:image/gif;base64,{data_url}" alt="car gif" style="width: 150px;">'
                    st.markdown(image_html, unsafe_allow_html=True)
                    st.write('\n')
                    st.markdown("That's the equivalent of driving **753km in car**")

                if choice == "1-2 times a week":
                    tofu_emissions = fod[fod['Entity'] == 'Tofu']
                    # Total emisions of 150g by 1,5 days week
                    total_emissions = tofu_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                        'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                        'food_emissions_packaging', 'food_emissions_losses']].sum().sum() * 0.15
                    # Result
                    st.write(f"Over an entire year your consumption of tofu is adding {math.ceil(total_emissions* 78)}kg greenhouse gas emissions.")
                    # GIF car
                    with open(r'..\images\streamlit\car.gif', 'rb') as r_ima:
                        contents = r_ima.read()
                    data_url = base64.b64encode(contents).decode("utf-8")
                    image_html = f'<img src="data:image/gif;base64,{data_url}" alt="car gif" style="width: 150px;">'
                    st.markdown(image_html, unsafe_allow_html=True)
                    st.write('\n')
                    st.markdown("That's the equivalent of driving **160km in car**")

                if choice == "Never":
                    tofu_emissions = fod[fod['Entity'] == 'Tofu']
                    # Total emisions of 60kg by year, global mean
                    total_emissions = tofu_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                        'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                        'food_emissions_packaging', 'food_emissions_losses']].sum().sum()
                    # Result
                    st.write(f"That's interesting, eventhough over an entire year the world average consumption of tofu is adding {math.ceil(total_emissions* 60)}kg greenhouse gas emissions.")
                    # GIF car
                    with open(r'..\images\streamlit\car.gif', 'rb') as r_ima:
                        contents = r_ima.read()
                    data_url = base64.b64encode(contents).decode("utf-8")
                    image_html = f'<img src="data:image/gif;base64,{data_url}" alt="car gif" style="width: 150px;">'
                    st.markdown(image_html, unsafe_allow_html=True)
                    st.write('\n')
                    st.markdown("That's the equivalent of driving **822km in car**")


    elif opcion == 'Vegetable oils':
        st.subheader("Let's dive into the world of vegetable oils")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write('\n')
            st.write("⚡**Fun fact**: There are **numerous types of vegetable oils** available, each derived from different plant sources. Some common examples include olive oil, canola oil, soybean oil, sunflower oil, and coconut oil. Each oil has its own distinct **flavor**, **smoke point**, and **nutritional profile**.")
            st.write('\n')
            st.write('\n')
            st.write("But not everything is sunshine 🌞 and rainbows 🌈. The production of vegetable oils can have both positive and negative environmental impacts. On the **positive side**, vegetable oils derived from sustainable sources, such as palm oil from certified plantations, can help reduce deforestation and preserve biodiversity. On the **negative side**, the expansion of oil palm plantations, particularly in tropical regions, has been associated with deforestation and habitat loss for endangered species.")

        with col2:
            st.image('../images/streamlit/oils.png')

        # Get the top 10 countries with highest production
        columns = ['Palm', 'Groundnut', 'Cottonseed', 'Coconut', 'Maize']
        for col in columns:
            oil_prod[col] = pd.to_numeric(oil_prod[col], errors='coerce')

        # Filter the data for the entity "Brasil"
        filtered_data = oil_prod[oil_prod['Entity'] == 'Brazil']

        # Create a line chart for each oil type
        col = ["#827717", "#FF8A65", "#FFCCBC", "#7CB342", "#DCE775"]
        fig = go.Figure()
        for i, oil_type in enumerate(['Palm', 'Groundnut', 'Cottonseed', 'Coconut', 'Maize']):
            fig.add_trace(go.Scatter(
                x=filtered_data['Year'],
                y=filtered_data[oil_type],
                mode='lines',
                name=oil_type,
                line=dict(color=col[i])
        ))

        # Set chart layout
        fig.update_layout(
            title='Production Evolution of Palm, Groundnut, Cottonseed, Coconut and Maize',
            xaxis_title='Year',
            yaxis_title='Yield',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )


        # Render the chart using Streamlit
        st.plotly_chart(fig, theme='streamlit', use_container_width=True)
        st.write("Over the years, we can witness the evolution of **production in terms of hectares** dedicated to oil harvest, with **palm oil** experiencing the most exponential growth. This trend highlights the alarming issue of **deforestation**, as it necessitates larger areas of land for these harvests, resulting in the destruction of native flora.")
        st.write("---")

        st.subheader("Emissions comparation between oils")
        st.write("Discover how each **oil type** contributes to greenhouse gas emissions and gain valuable insights into their **sustainability**. Start comparing now and make informed decisions for a greener future!")

        # Define the data and buttons
        oils = ['Olive Oil', 'Palm Oil', 'Rapeseed Oil', 'Soybean Oil', 'Sunflower Oil']

        # Filters
        selected_oils = st.multiselect("Which oils do you use the most:", oils)
        filtered_data = fod[fod['Entity'].isin(selected_oils)]

        # Create a list of emissions columns
        emissions_columns = ['food_emissions_land_use', 'food_emissions_farm',
                            'food_emissions_processing',
                            'food_emissions_packaging', 'food_emissions_losses']


        # Create the radial chart for the selected oils
        fig = go.Figure()

        col_lin = ["#FFAB00", "#827717", "#BF360C", "#FF3D00", "#AFB42B",]
        col_fil = ["rgba(255, 171, 0, 0.5)", "rgba(130, 119, 23, 0.5)", "rgba(191, 54, 12, 0.5)", "rgba(255, 61, 0, 0.5)", "rgba(175, 180, 43, 0.5)"]

        for i, oil in enumerate(selected_oils):
            fig.add_trace(go.Scatterpolar(
                r=filtered_data.loc[filtered_data['Entity'] == oil, emissions_columns].values[0],
                theta=emissions_columns,
                fill='toself',
                name=oil,
                fillcolor=col_fil[i % len(col_fil)],
                line_color=col_lin[i % len(col_lin)]
            ))

        fig.update_layout(
            polar=dict(
                bgcolor='#dcffc4',
                radialaxis=dict(visible=True),
            ),
            showlegend=True,
            paper_bgcolor=None,
        )

        # Render the chart using Streamlit
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')

        st.write("**Legend**:")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.write("- emissions_processing: CO2e by the processing.")
        with col2: 
            st.write("- emissions_packaging: CO2e by the packaging.")
        with col3:
            st.write("- emissions_losses: CO2e by losses.")
        with col4:
            st.write("- emissions_land_use: CO2e by the harvest.")
        with col5:
            st.write("- emissions_farm: CO2e by the farm.")


    elif opcion == 'Meat':
        st.subheader("Let's dive into the world of meat")
        st.write("Is animal protein better that vegetal protein?")




    elif opcion == 'Take your pick!':

        ruta = r'../images/streamlit/table.png'
        st.image(ruta, use_column_width=True)




    else:
       
        col1, col2, col3 = st.columns(3)

        with col1:
           st.write('\n')
        with col2:
            with st.spinner("Loading..."):
                time.sleep(5)

            st.write("**⚠️⚠️⚠️ Error 502 ⚠️⚠️⚠️**")
            st.write("**Ups! There seems to be a problem... Please, try again later.**")
            st.image('../images/streamlit/tofuangry.png', width=250)

if selected == 'Recomendations':

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.write('               ')
    with col2:
        st.image('../images/streamlit/logof.png', width=210)


    st.subheader('Are you ready to embrace change?')

    recom = st.radio(r"Here we guide a few rutine changes to reduce our annual print. Select the options and check them :)",
    ('Climate-Friendly Food', 'Organic and Sustainable Certifications', 'Waste Reduction', 'Local Food'))

    st.write('---')
    if recom == 'Climate-Friendly Food':

        st.write('\n')
        st.markdown("""
            🥦**Climate-Friendly Food**")
            - High-energy and processed foods contribute to more global warming pollution.
            - The carbon footprint of meat, especially from ruminant animals, is significant due to methane emissions.
            - Seafood, particularly large fish stocks, contribute to global warming pollution and may contain mercury.""")
        st.write('\n')
        st.write('\n')
        st.markdown("""
            ✊🏼**Action Steps**:

            - Eat lower on the food chain by adding more fruits, vegetables, and grains to your diet and reducing red meat consumption.
            - Choose locally caught and sustainably managed fish or herbivorous farmed stocks.
            - Opt for fresh foods with minimal processing and avoid excessive freezing, packaging, and refrigeration.""")
    elif recom == 'Organic and Sustainable Certifications':
        st.markdown("""
            ♻️**Organic and Sustainable Certifications**:
            - Eco-labels like USDA Organic reward environmental performance.
            - Organic agriculture reduces global warming pollution and avoids synthetic pesticides and fertilizers.""")
        st.write('\n')
        st.write('\n')
        st.markdown("""
            ✊🏼**Action Steps**:

            - Purchase organic and certified foods whenever possible.
            - Refer to reputable sources like Consumer Reports for guidance on eco-labels.""")

    elif recom == 'Waste Reduction':
        st.write('\n')
        st.markdown("""
            🔅**Waste Reduction**:
            - A significant portion of food produced in the US is wasted, leading to environmental impacts and greenhouse gas emissions.
            - Food waste in landfills releases methane, a potent heat-trapping gas.""")
        st.write('\n')
        st.write('\n')
        st.markdown("""
            ✊🏼**Action Steps**:

            - Buy and consume foods before they expire to minimize waste.
            - Compost food waste to reduce greenhouse gas emissions and the need for synthetic fertilizers.""")
    else:
        st.write('\n')
        st.markdown("""
            🌾**Local Food**:
            - Meals often contain ingredients from multiple foreign countries, with domestically grown produce traveling long distances.
            - Buying locally reduces pollution and energy use associated with food transportation.""")
        st.write('\n')
        st.write('\n')
        st.markdown("""
            ✊🏼**Action Steps**:

            - Choose local food options and avoid purchasing food imported by airplane.
            - Consider the environmental significance of food type and production methods.""")


if selected == 'About us':

    st.header('Who are we?')

    col1, col2 = st.columns(2)
    with col1:
        st.write("This is a project made in Ironhack to practice all the process of a data analyst. It was processed with Streamlit.")
    with col2:
        st.write("Hi! My name is Nerea. I´m a data analyst passioned about social studies.")
        st.write("You can see more of my work here: ")
        st.write("[Check my github](https://github.com/NereaRiveiro)")
    