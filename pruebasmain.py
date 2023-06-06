import streamlit as st

from notebook.funciones import *
import pandas as pd
import numpy as np
import math
from itertools import cycle

pd.options.plotting.backend = "plotly"
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib.animation import FuncAnimation


st.set_page_config(page_title="Go vegan?", page_icon=":avocado:", layout="wide", initial_sidebar_state="expanded")


fod = pd.read_csv(r'.\data\Food\food_clean.csv')
soy = pd.read_csv(r'.\data\Soy\soy_clean.csv', parse_dates=['Year'])
oil_prod = pd.read_csv(r'.\data/Palm/oil_prod_clean.csv')
oil_yield = pd.read_csv(r'.\data/Palm/oil_yield_clean.csv')
pop = pd.read_csv(r'.\data/Population/population_clean.csv')

# filtro para sacar lista de sólo paises
todos = soy['Entity'].value_counts().index.to_list()
paises = filtrar_paises(todos)

palette = ['#6a863b', '#68c843', '#f39f18']

# Configuración del color de fondo
with open('style.css') as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )


def main():
    st.title("Go vegan?")

if __name__ == '__main__':
    main()

st.header("Are you aware of your impact?")
st.subheader("Discover your food choices environmental impact")
st.write("We´ve extracted info about the 40 foods most tipical around the world. Let´s check some info")


# Gráfico de todas las food
# Cálculo de las emisiones totales de comida
fod['Total_Food_Emissions'] = fod.iloc[:, 2:9].sum(axis=1)

# Ordenar el DataFrame por las emisiones totales
df_sorted = fod.sort_values('Total_Food_Emissions', ascending=True)

# Lista de colores
n_colors = 43  # Número deseado de colores
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


# Food specifications
food_l = ["Take your pick!" ,"Beef", "Palm oil", "Soy"]
opcion = st.selectbox('Which food are you interested in the most?', food_l)
st.write("You´ve chosen", opcion)

if opcion == 'Soy':

    st.write("**Fun fact**: There are health benefits to soy, which include providing a good source of *heart-healthy fats*, *fiber*, *potassium* and *iron*.")
    st.write("But not everything is sunshine 🌞 and rainbows 🌈. Soy is one of the main causes of deforestation in South America. But, what for is destined the soybean production?")

    # Comparative graphic between soybeans for food, feed or processed
    # new df filtered from 2000
    df = soy[soy['Year'].dt.year >= 2000]

    # Sum of values
    totals = df[['Food', 'Feed', 'Processed']].sum()

    # Colors and labels
    colors = ['#FF5722', '#AED581', '#D0ECE7']
    labels = ['Food', 'Feed', 'Processed']

    # Create figure
    fig = go.Figure()

    # Crear las barras animadas
    for i in range(len(labels)):
        fig.add_trace(
            go.Bar(
                x=[labels[i]],
                y=[0],
                marker=dict(color=colors[i]),
                name=labels[i],
                hovertemplate=f'{labels[i]}: 0',
            )
        )
        fig.update_traces(overwrite=True)  # Actualizar las barras en cada iteración
        fig.update_layout(
            updatemenus=[dict(
                type='buttons',
                showactive=False,
                buttons=[dict(
                    label='Play',
                    method='animate',
                    args=[None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}]
            )]
        )
    ]
)
    # Actualizar las barras en cada fotograma de la animación
    frames = []
    for i in range(len(labels)):
        frame_data = df[labels[i]].tolist()  # Obtener los datos correspondientes a la categoría actual
        frames.append(go.Frame(data=[go.Bar(y=[frame_data[j]], hovertemplate=f'{labels[i]}: {frame_data[j]}') for j in range(len(frame_data))]))

    fig.frames = frames

    # Configurar el diseño del gráfico
    fig.update_layout(
        title='Total emissions by category',
        xaxis=dict(
            title='Category',
            title_font=dict(color='#59412f')),
        yaxis=dict(
            title='Total emissions',
            title_font=dict(color='#59412f'),
            range=[0, max(totals) + max(totals) * 0.1]),
        height=400,
        width=600,
        showlegend=False,
    )

    # Config exe y
    fig.update_yaxes(
        tickfont=dict(color='#6C584C'))

    # Congif exe x
    fig.update_xaxes(
        tickfont=dict(color='#7E675E'))

    # Mostrar el gráfico animado
    st.plotly_chart(fig, use_container_width=True)



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

    st.write(f'a verrrrrrrrrrrrrrrrrrrrrrrrrr', len(df_top_countries['Entity']))
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
    colors = sns.color_palette('pastel')  # Colores de la paleta 'pastel' de Seaborn
    colors = [f'rgb({int(color[0] * 255)},{int(color[1] * 255)},{int(color[2] * 255)})' for color in colors]
    for i, year in enumerate(df_top_countries['Year'].unique()):
        frame_data = df_top_countries[df_top_countries['Year'] <= year]
        frame = go.Frame(
            data=[go.Scatter(x=frame_data[frame_data['Entity'] == country]['Year'], 
                            y=frame_data[frame_data['Entity'] == country]['Area harvested'], 
                            mode='lines', 
                            name=country,
                            line=dict(color=colors[i]))  # Asignar color de la paleta
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
    st.plotly_chart(fig)

    st.write("In Brazil the production in 2020 was by 370k hectares. That´s the equivalent for 370k football fields or the whole surface of Mexico City")


    # Tofu and soy milk consumption
    list_soy = ["Choose an option", "Soy milk", "Tofu"]
    soy_choice = st.selectbox("The most common human foods made by soy are soy milk and tofu, let´s check them!", list_soy)
    # SOY MILK
    if soy_choice == 'Soy milk':

        freq = ["Are you an usual consumer?" ,"Once a day", "1-2 times a week", "Never"]
        soymilk_choice = st.selectbox("How often do you have it?", freq)
        if soymilk_choice == "Once a day":
            soy_milk_emissions = fod[fod['Entity'] == 'Soy milk']
            # Total emisions of 200g by day
            total_emissions = soy_milk_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                'food_emissions_packaging', 'food_emissions_losses']].sum().sum() * 0.2
            # Result
            st.write(f"Over an entire year your consumption of soy milk is adding {math.ceil(total_emissions* 365)}kg greenhouse gas emissions.")
        if soymilk_choice == "1-2 times a week":
            soy_milk_emissions = fod[fod['Entity'] == 'Soy milk']
            # Total emisions of 200g by1,5 days week
            total_emissions = soy_milk_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                'food_emissions_packaging', 'food_emissions_losses']].sum().sum() * 0.2
            # Result
            st.write(f"Over an entire year your consumption of soy milk is adding {math.ceil(total_emissions* 78)}kg greenhouse gas emissions.")
        if soymilk_choice == "Never":
            soy_milk_emissions = fod[fod['Entity'] == 'Soy milk']
            # Total emisions of 42kg by year, global mean
            total_emissions = soy_milk_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                'food_emissions_packaging', 'food_emissions_losses']].sum().sum()
            # Result
            st.write(f"Over an entire year your consumption of soy milk is adding {math.ceil(total_emissions* 42)}kg greenhouse gas emissions.")
    
    # TOFU
    if soy_choice == 'Tofu':
        col1, col2 = st.columns([1, 2])
        # imagen tofu
        with col1:
            ruta_imagen = r'.\images\tofua.png'
            st.image(ruta_imagen, width=150, clamp=True)

        with col2:
            freq = ["Are you an usual consumer?", "Once a day", "1-2 times a week", "Never"]
            # consumption                
            tofu_choice = st.selectbox("How often do you have it?", freq)
            if tofu_choice == "Once a day":
                tofu_emissions = fod[fod['Entity'] == 'Tofu']
                # Total emisions of 150g by day
                total_emissions = tofu_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                    'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                    'food_emissions_packaging', 'food_emissions_losses']].sum().sum() * 0.15
                # Result
                st.write(f"Over an entire year your consumption of tofu is adding {math.ceil(total_emissions* 365)}kg greenhouse gas emissions.")  
            if tofu_choice == "1-2 times a week":
                tofu_emissions = fod[fod['Entity'] == 'Tofu']
                # Total emisions of 150g by 1,5 days week
                total_emissions = tofu_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                    'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                    'food_emissions_packaging', 'food_emissions_losses']].sum().sum() * 0.15
                # Result
                st.write(f"Over an entire year your consumption of tofu is adding {math.ceil(total_emissions* 78)}kg greenhouse gas emissions.")
            if tofu_choice == "Never":
                tofu_emissions = fod[fod['Entity'] == 'Tofu']
                # Total emisions of 60kg by year, global mean
                total_emissions = tofu_emissions[['food_emissions_land_use', 'food_emissions_farm', 'food_emissions_animal_feed',
                                                    'food_emissions_processing', 'food_emissions_transport', 'food_emissions_retail',
                                                    'food_emissions_packaging', 'food_emissions_losses']].sum().sum()
                # Result
                st.write(f"Over an entire year your consumption of tofu is adding {math.ceil(total_emissions* 60)}kg greenhouse gas emissions.")

if st.button("Click here!"):
    st.write("¡Presionaste el botón!")
