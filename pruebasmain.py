import streamlit as st

import pandas as pd
import plotly.express as px
import seaborn as sns

def main():
    st.title("Pruebas")

if __name__ == '__main__':
    main()


st.header("Go vegan?")
st.subheader("Discover your food choices environmental impact")
st.text("Are you ready for some fun?")


nombre = st.text_input("What's your name?")
st.write("¡Hi,", nombre, "!")



opcion = st.selectbox("Which one do you like most", ["Beef", "Palm oil", "Soy"])
st.write("You´ve chosen", opcion)

if opcion == 'Soy':
    soy = pd.read_csv('.\data\Soy\soy_clean.csv')
    fig = px.scatter(soy, x='Entity', y='Feed', color='Year')
    st.plotly_chart(fig)

if st.button("Click here!"):
    st.write("¡Presionaste el botón!")
