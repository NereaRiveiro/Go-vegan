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
st.text("We´ve extracted info abaout the 40 foods more tipical around the world. Let´s check some info")


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
    title='Suma de Emisiones de Alimentos por Entidad',
    xaxis_title='Total de Emisiones de Alimentos',
    yaxis_title='Entidad',
    legend=dict(x=1.02, y=1),
    height=500,
    width=800
)

st.plotly_chart(fig)



nombre = st.text_input("What's your name?")
st.write("¡Hi,", nombre, "!")



opcion = st.selectbox("Which one are you interested in the most?", ["Beef", "Palm oil", "Soy"])
st.write("You´ve chosen", opcion)

if opcion == 'Soy':
    fig = px.scatter(soy, x='Entity', y='Feed', color='Year')
    st.plotly_chart(fig)

    # Gráfico de hectáreas por países



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

if st.button("Click here!"):
    st.write("¡Presionaste el botón!")
