import streamlit as st

from notebook.funciones import *
import pandas as pd
import numpy as np
pd.options.plotting.backend = "plotly"
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib.animation import FuncAnimation


fod = pd.read_csv(r'Go-vegan-\data\Food\food_clean.csv')
soy = pd.read_csv(r'Go-vegan-\data\Soy\soy_clean.csv', parse_dates=['Year'])
oil_prod = pd.read_csv(r'Go-vegan-\data/Palm/oil_prod_clean.csv')
oil_yield = pd.read_csv(r'Go-vegan-\data/Palm/oil_yield_clean.csv')
pop = pd.read_csv(r'Go-vegan-\data/Population/population_clean.csv')

# filtro para sacar lista de sólo paises
todos = soy['Entity'].value_counts().index.to_list()
paises = filtrar_paises(todos)

palette = ['#6a863b', '#68c843', '#f39f18']

st.markdown(
    f"""
    <style>
    body {{
        font-family: 'Arial', monospace;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("Go vegan?")

if __name__ == '__main__':
    main()

st.header("Are you aware of your impact?")
st.subheader("Discover your food choices environmental impact")
st.write("We´ve extracted info about the 40 foods most tipical around the world. Let´s check some info")


# Gráfico de todas las food
fod['Total_Food_Emissions'] = fod.iloc[:, 2:9].sum(axis=1)

df_sorted = fod.sort_values('Total_Food_Emissions', ascending=True)

colors = sns.color_palette('pastel')

# Gráfico de barras horizontales
fig = go.Figure(data=go.Bar(
    x=df_sorted['Total_Food_Emissions'],
    y=df_sorted['Entity'],
    orientation='h',
    marker=dict(color=colors)
))

fig.update_layout(
    title='Global CO emisions by food',
    xaxis_title='Total emisions',
    yaxis_title='Food',
    legend=dict(x=1.02, y=1),
    height=500,
    width=800
)

st.plotly_chart(fig)



nombre = st.text_input("What's your name?")
st.write("¡Hi,", nombre, "!")


# Food specifications
opcion = st.selectbox("Which food are you interested in the most?", ["Beef", "Palm oil", "Soy"])
st.write("You´ve chosen", opcion)

if opcion == 'Soy':

    st.write("**Fun fact**: There are health benefits to soy, which include providing a good source of *heart-healthy fats*, *fiber*, *potassium* and *iron*.")
    st.write("But not everything is sunshine 🌞 and rainbows 🌈. Soy is one of the main causes of deforestation in South America. But, what for is destined the soybean production?")

    # Comparative graphic between soybeans for food, feed or processed
    df = soy[soy['Year'].dt.year >= 2000]
    # Sum "Food", "Feed" y "Processed"
    totals = df[['Food', 'Feed', 'Processed']].sum()
    # Figure
    fig, ax = plt.subplots()
    x_labels = ['Food', 'Feed', 'Processed']
    x = range(len(x_labels))
    bars = ax.bar(x, totals)
    # Labels in bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height,
                f'{height}', ha='center', va='bottom')
    # Labels x exe
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    # Show
    st.plotly_chart(fig)

    st.write("Wow! The difference between them are surprising. Some examples from what soy can be processed are soy oil and soybean cake for basic animal feed protein")

    st.write("Where are these macroharvest?")
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
        xaxis=dict(range=[df_top_countries['Year'].min(), df_top_countries['Year'].max()], autorange=False),
        updatemenus=[
            dict(
                type='buttons',
                buttons=[
                    dict(label='Reproducir',
                        method='animate',
                        args=[None, {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 500}}]),
                    dict(label='Pausa',
                        method='animate',
                        args=[[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}])
                ],
                active=0,
                showactive=True,
                x=0.05,
                y=0,
                xanchor='right',
                yanchor='bottom'
            )
        ]
    )
    # Animation photograms
    frames = []
    for year in df_top_countries['Year'].unique():
        frame_data = df_top_countries[df_top_countries['Year'] == year]
        frame = go.Frame(
            data=[go.Scatter(x=frame_data['Year'], y=frame_data['Area harvested'], mode='lines', name=country)
                for country in top_countries],
            name=str(year)
        )
        frames.append(frame)
    fig.frames = frames
    # Show
    st.plotly_chart(fig)

    st.write("In Brazil the production in 2020 was by 370k hectares. That´s the equivalent for 370k football fields or the whole surface of Mexico City")


    # Tofu and soy milk consumption
    soy_choice = st.selectbox("The most common human foods made by soy are soy milk and tofu, let´s check them!", ["Soy milk", "Tofu"])
    if soy_choice == 'Soy milk':
        soymilk_choice = st.selectbox("how often do you have it?", ["Once a day", "1-2 times a week", "Never"])
        if soymilk_choice == "Once a day":
            soy_milk_emissions = fod[fod['Entity'] == 'Soy milk']
            # Total emisions of 200g by day
            total_emissions = soy_milk_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                'food_emissions_packaging', 'food_emissions_losses']].sum().sum() * 0.2
            # Result
            st.write("Total emisions of Soy milk by year", total_emissions.round(2)* 365)
        if soymilk_choice == "1-2 times a week":
            soy_milk_emissions = fod[fod['Entity'] == 'Soy milk']
            # Total emisions of 200g by1,5 days week
            total_emissions = soy_milk_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                'food_emissions_packaging', 'food_emissions_losses']].sum().sum() * 0.2
            # Result
            st.write("Total emisions of Soy milk by year", total_emissions.round(2)* 78)
        if soymilk_choice == "Never":
            soy_milk_emissions = fod[fod['Entity'] == 'Soy milk']
            # Total emisions of 42kg by year, global mean
            total_emissions = soy_milk_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                'food_emissions_packaging', 'food_emissions_losses']].sum().sum()
            # Result
            st.write("Total emisions of Soy milk by year", total_emissions.round(2)* 42)

    if soy_choice == 'Tofu':
        soymilk_choice = st.selectbox("how often do you have it?", ["Once a day", "1-2 times a week", "Never"])
        if soymilk_choice == "Once a day":
            soy_milk_emissions = fod[fod['Entity'] == 'Tofu']
            # Total emisions of 150g by day
            total_emissions = soy_milk_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                'food_emissions_packaging', 'food_emissions_losses']].sum().sum() * 0.15
            # Result
            st.write("Total emisions of tofu by year", total_emissions.round(2)* 365)
        if soymilk_choice == "1-2 times a week":
            soy_milk_emissions = fod[fod['Entity'] == 'Tofu']
            # Total emisions of 150g by 1,5 days week
            total_emissions = soy_milk_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                'food_emissions_packaging', 'food_emissions_losses']].sum().sum() * 0.15
            # Result
            st.write("Total emisions of tofu by year", total_emissions.round(2)* 78)
        if soymilk_choice == "Never":
            soy_milk_emissions = fod[fod['Entity'] == 'Tofu']
            # Total emisions of 60kg by year, global mean
            total_emissions = soy_milk_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                'food_emissions_packaging', 'food_emissions_losses']].sum().sum()
            # Result
            st.write("Total emisions of tofu by year", total_emissions.round(2)* 60)

if st.button("Click here!"):
    st.write("¡Presionaste el botón!")
